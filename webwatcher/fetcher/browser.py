import logging
import time
from contextlib import closing, contextmanager

import html2text
from selenium import webdriver
from xvfbwrapper import Xvfb


logger = logging.getLogger(__name__)


def browser(conf):
    url = conf['url']
    output_format = conf.get('format', 'html')
    delay = conf.get('delay')
    tag_name = conf.get('tag')
    xpath = conf.get('xpath', '//*')
    scenario = conf.get('scenario')
    with firefox() as driver:
        driver.get(url)
        if scenario:
            run_scenario(driver, scenario)
        if delay:
            time.sleep(delay)
        if tag_name:
            elem = driver.find_element_by_tag_name(tag_name)
            html = elem.get_attribute('outerHTML')
        else:
            elem = driver.find_element_by_xpath(xpath)
            html = elem.get_attribute('outerHTML')
        if output_format == 'text':
            return sanitize(html)
        elif output_format == 'html':
            return html


def sanitize(html):
    return html2text.html2text(html)


@contextmanager
def virtual_buffer():
    """
    Try to start xvfb, trying multiple (up to 5) times if a failure
    """
    for i in range(0, 6):
        xvfb_display = Xvfb()
        xvfb_display.start()
        # If Xvfb started, return.
        if xvfb_display.proc is not None:
            try:
                yield
                return
            finally:
                xvfb_display.stop()
    raise Exception("Xvfb could not be started after six attempts.")


@contextmanager
def firefox():
    with virtual_buffer():
        with closing(webdriver.Firefox()) as driver:
            yield driver


def run_scenario(driver, code):
    logger.info("Executing custom scenario")
    logger.debug(code)
    exec(code, {'driver': driver})
