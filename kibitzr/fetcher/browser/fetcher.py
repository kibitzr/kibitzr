import os
import time
import shutil
import logging
import traceback
import collections

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from jinja2 import Template

from kibitzr.conf import settings
from .launcher import firefox, PROFILE_DIR
from .trigger import prompt_return


logger = logging.getLogger(__name__)
HOME_PAGE = 'https://kibitzr.github.io/'


def persistent_firefox():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    print("Kibitzr is running Firefox in persistent profile mode.")
    with firefox(headless=False) as driver:
        driver.get(HOME_PAGE)
        while True:
            prompt_return()
            try:
                # Property raises when browser is closed:
                driver.title
            except:
                # All kinds of things happen when closing Firefox
                break
            else:
                update_profile(driver)
                print(
                    "Firefox profile is saved. "
                    "Close browser now to reuse profile in further runs."
                )
    print(
        "Firefox is closed. "
        "To delete saved profile remove following directory: "
        f"{os.path.abspath(PROFILE_DIR)}"
    )


def update_profile(driver):
    if os.path.exists(PROFILE_DIR):
        shutil.rmtree(PROFILE_DIR)
    shutil.copytree(
        driver.capabilities['moz:profile'],
        PROFILE_DIR,
        ignore=shutil.ignore_patterns(
            "parent.lock",
            "lock",
            ".parentlock",
            "*.sqlite-shm",
            "*.sqlite-wal",
        ),
    )


def firefox_fetcher(conf):
    headless = conf.get('headless', True)
    with firefox(headless) as driver:
        fetcher = FirefoxFetcher(driver)
        return fetcher.fetch(conf)


class FirefoxFetcher:

    def __init__(self, driver):
        self.driver = driver

    def fetch(self, conf):
        """
        1. Fetch URL
        2. Run automation.
        3. Return HTML.
        4. Close the tab.
        """
        url = conf['url']
        # If Firefox is broken, it will raise here, causing kibitzr restart:
        self.driver.set_window_size(1366, 800)
        self.driver.implicitly_wait(2)
        self.driver.get(url)
        try:
            self._run_automation(conf)
            html = self._get_html()
        except:
            logger.exception(
                "Exception occurred while fetching"
            )
            return False, traceback.format_exc()
        finally:
            self._close_tab()
        return True, html

    def _run_automation(self, conf):
        """
        1. Fill form.
        2. Run scenario.
        3. Delay.
        """
        self._fill_form(self._find_form(conf))
        self._run_scenario(conf)
        self._delay(conf)

    @staticmethod
    def _fill_form(form):
        """
        Fill all inputs with provided Jinja2 templates.
        If no field had click key, submit last element.
        """
        clicked = False
        last_element = None
        for field in form:
            if field['text']:
                field['element'].clear()
                field['element'].send_keys(field['text'])
            if field['click']:
                field['element'].click()
                clicked = True
            last_element = field['element']
        if last_element:
            if not clicked:
                last_element.submit()

    def _find_form(self, conf):
        """
        Find elements defined in conf['form'].
        Render all Jinja2 templates from field['value'].
        Save all field['click'] triggers.
        If all found, return them as a list of dictionaries.
        If at least one was not found, return empty list.
        """
        form = conf.get('form', [])
        fields = []
        creds = settings().creds
        first_field = True
        for field in form:
            click = field.get('click')
            text = self._parse_field_text(field, conf, creds)
            selector_type, selector = self._parse_field_selector(field)
            if selector:
                element = self._find_element(
                    selector,
                    selector_type,
                    check_displayed=first_field,
                )
                if element:
                    fields.append({
                        'element': element,
                        'text': text,
                        'click': click,
                    })
                else:
                    logging.warning("Element {%s: %s} not found",
                                    selector_type, selector)
            else:
                logging.warning("Failed to parse selector %r", field)
            first_field = False
        if len(fields) == len(form):
            return fields
        logging.info(
            "Skipped form filling because not all fields were found"
        )
        return []

    @staticmethod
    def _parse_field_selector(field):
        """
        Check field keys: css, xpath and id.
        Return the first found along with it's value.
        """
        for selector_type in ('css', 'xpath', 'id'):
            selector = field.get(selector_type)
            if selector:
                return selector_type, selector
        logger.warning("Form field does not define any selector "
                       "(id, css and xpath available): %r",
                       field)
        return None, None

    @staticmethod
    def _parse_field_text(field, conf, creds):
        """
        Return form field value from 3 options:
        1. If value key is present, render it as a Jinja2 template.
           The template has access to ``conf`` and ``creds`` dictionaries.
        2. If creds key is present, use it as a dot-delimited path
           in creds dictionary (e.g. ``account.login``).
        3. Otherwise return None
        """
        value = field.get('value')
        if value:
            template = Template(value)
            return template.render(
                conf=conf,
                creds=creds,
            )
        creds_path = field.get('creds')
        if creds_path:
            bread_crumbs = creds_path.split('.')
            node = creds
            for crumb in bread_crumbs:
                node = node[crumb]
            return node
        return None

    def _run_scenario(self, conf):
        scenario = conf.get('scenario')
        if isinstance(scenario, collections.abc.Mapping):
            code = scenario['python']
            elements = scenario.get('elements', {})
        else:
            code = scenario
            elements = {}
        if elements:
            element_objects = self._find_elements(elements)
        else:
            element_objects = {}
        if code:
            self._exec_scenario(code, conf, element_objects)

    @staticmethod
    def _delay(conf):
        delay = conf.get('delay')
        if delay:
            time.sleep(delay)

    def _get_html(self):
        total_attempts = 3
        for attempt in range(1, total_attempts + 1):
            try:
                elem = self.driver.find_element(By.XPATH, "//*")
                html = elem.get_attribute("outerHTML")
            except (NoSuchElementException, StaleElementReferenceException):
                # Crazy (but stable) race condition,
                # new page loaded after call to find_element
                # Just retry:
                if attempt == total_attempts:
                    raise
                time.sleep(1)
            else:
                if html is None:
                    if attempt == total_attempts:
                        html = ""
                    else:
                        time.sleep(1)
                        continue
                return html
        return None

    def _find_elements(self, elements):
        logger.info("Finding elements")
        result = {}
        for key, selector in elements.items():
            name, _, selector_type = key.partition("|")
            result[name] = self._find_element(selector, selector_type.lower())
        return result

    def _find_element(self, selector, selector_type, check_displayed=False):
        """
        Return first matching displayed element of non-zero size
        or None if nothing found
        """
        if selector_type == 'css':
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        elif selector_type == 'xpath':
            elements = self.driver.find_elements(By.XPATH, selector)
        elif selector_type == 'id':
            elements = self.driver.find_elements(By.CSS_SELECTOR, '#' + selector)
        else:
            raise RuntimeError(
                f"Unknown selector_type: {selector_type} for selector: {selector}"
            )
        for element in elements:
            if check_displayed:
                if not element.is_displayed() or sum(element.size.values()) <= 0:
                    continue
            return element

    def _exec_scenario(self, code, conf, elements):
        logger.info("Executing custom scenario")
        logger.debug(code)
        exec(  # pylint: disable=exec-used
            code,
            {
                'conf': conf,
                'creds': settings().creds,
                'driver': self.driver,
                'elements': elements,
                'By': By,
            },
        )

    def _close_tab(self):
        """
        Create a new tab and close the old one
        to avoid idle page resource usage
        """
        old_tab = self.driver.current_window_handle
        self.driver.execute_script('''window.open("about:blank", "_blank");''')
        self.driver.switch_to.window(old_tab)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
