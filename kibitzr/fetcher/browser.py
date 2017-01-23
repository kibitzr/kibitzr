import logging
import time
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from xvfbwrapper import Xvfb
from ..conf import settings


logger = logging.getLogger(__name__)


firefox_instance = {
    'xvfb_display': None,
    'driver': None,
    'headed_driver': None,
}


def cleanup():
    """Must be called before exit"""
    global firefox_instance
    if firefox_instance['driver'] is not None:
        firefox_instance['driver'].quit()
        firefox_instance['driver'] = None
    if firefox_instance['headed_driver'] is not None:
        firefox_instance['headed_driver'].quit()
        firefox_instance['headed_driver'] = None
    if firefox_instance['xvfb_display'] is not None:
        firefox_instance['xvfb_display'].stop()
        firefox_instance['xvfb_display'] = None


def firefox_fetcher(conf):
    url = conf['url']
    delay = conf.get('delay')
    scenario = conf.get('scenario')
    headless = conf.get('headless', True)
    with firefox(headless) as driver:
        driver.get(url)
        if scenario:
            run_scenario(driver, scenario)
        if delay:
            time.sleep(delay)
        html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
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
        firefox_instance[driver_key] = webdriver.Firefox(
            firefox_binary=firefox_binary,
        )
        firefox_instance[driver_key].set_window_size(1024, 768)
    yield firefox_instance[driver_key]


def virtual_buffer():
    """
    Try to start xvfb, trying multiple (up to 5) times if a failure
    """
    for i in range(0, 6):
        xvfb_display = Xvfb()
        xvfb_display.start()
        # If Xvfb started, return.
        if xvfb_display.proc is not None:
            return xvfb_display
    raise Exception("Xvfb could not be started after six attempts.")


def run_scenario(driver, code):
    logger.info("Executing custom scenario")
    logger.debug(code)
    exec(code, {'driver': driver, 'creds': settings().creds})
