import os
import sys
import time
import shutil
import logging
from contextlib import contextmanager

from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import (
    WebDriverException,
    StaleElementReferenceException,
)

from ..conf import settings


logger = logging.getLogger(__name__)
PROFILE_DIR = 'firefox_profile'
HOME_PAGE = 'https://kibitzr.github.io/'


firefox_instance = {
    'xvfb_display': None,
    'driver': None,
    'headed_driver': None,
}


def cleanup():
    """Must be called before exit"""
    global firefox_instance
    temp_dirs = []
    if firefox_instance['driver'] is not None:
        if firefox_instance['driver'].profile:
            temp_dirs.append(firefox_instance['driver'].profile.profile_dir)
        firefox_instance['driver'].quit()
        firefox_instance['driver'] = None
    if firefox_instance['headed_driver'] is not None:
        if firefox_instance['headed_driver'].profile:
            temp_dirs.append(firefox_instance['headed_driver'].profile.profile_dir)
        firefox_instance['headed_driver'].quit()
        firefox_instance['headed_driver'] = None
    if firefox_instance['xvfb_display'] is not None:
        firefox_instance['xvfb_display'].stop()
        firefox_instance['xvfb_display'] = None
    for temp_dir in temp_dirs:
        shutil.rmtree(temp_dir, ignore_errors=True)


def persistent_firefox():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    with firefox(headless=False) as driver:
        driver.get(HOME_PAGE)
        while True:
            try:
                # Property raises when browser is closed:
                driver.title
            except (WebDriverException, OSError) as exc:
                break
            else:
                time.sleep(0.2)
        update_profile(driver)


def update_profile(driver):
    if os.path.exists(PROFILE_DIR):
        shutil.rmtree(PROFILE_DIR)
    shutil.copytree(
        driver.profile.profile_dir,
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
    url = conf['url']
    delay = conf.get('delay')
    scenario = conf.get('scenario')
    headless = conf.get('headless', True)
    with firefox(headless) as driver:
        driver.get(url)
        if scenario:
            old_root = driver.find_element_by_xpath("//*")
            run_scenario(driver, scenario, conf)
        if delay:
            time.sleep(delay)
        elem = driver.find_element_by_xpath("//*")
        try:
            html = elem.get_attribute("outerHTML")
        except StaleElementReferenceException:
            # Crazy (but stable) race condition,
            # new page loaded after call to find_element_by_xpath
            # Just retry:
            if elem.id == old_root.id:
                elem = driver.find_element_by_xpath("//*")
                html = elem.get_attribute("outerHTML")
        # Create a new tab and close the old one
        # to avoid idle page resource usage
        old_tab = driver.current_window_handle
        driver.execute_script('''window.open("about:blank", "_blank");''')
        driver.switch_to.window(old_tab)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True, html


@contextmanager
def firefox(headless=True):
    global firefox_instance
    if headless:
        if firefox_instance['xvfb_display'] is None:
            firefox_instance['xvfb_display'] = virtual_buffer()
        driver_key = 'driver'
    else:
        driver_key = 'headed_driver'
    if firefox_instance[driver_key] is None:
        if logger.level == logging.DEBUG:
            firefox_binary = FirefoxBinary(log_file=sys.stdout)
        else:
            firefox_binary = None
        # Load profile, if it exists:
        if os.path.isdir(PROFILE_DIR):
            firefox_profile = webdriver.FirefoxProfile(PROFILE_DIR)
        else:
            firefox_profile = None
        firefox_instance[driver_key] = webdriver.Firefox(
            firefox_binary=firefox_binary,
            firefox_profile=firefox_profile,
        )
        firefox_instance[driver_key].set_window_size(1024, 768)
    yield firefox_instance[driver_key]


def virtual_buffer():
    """
    Try to start xvfb, trying multiple (up to 5) times if a failure
    """
    for _ in range(0, 6):
        xvfb_display = Xvfb()
        xvfb_display.start()
        # If Xvfb started, return.
        if xvfb_display.proc is not None:
            return xvfb_display
    raise Exception("Xvfb could not be started after six attempts.")


def run_scenario(driver, code, conf):
    logger.info("Executing custom scenario")
    logger.debug(code)
    exec(
        code,
        {
            'conf': conf,
            'creds': settings().creds,
            'driver': driver,
        },
    )
