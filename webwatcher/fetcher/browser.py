import logging
import time
from contextlib import contextmanager

from selenium import webdriver
from xvfbwrapper import Xvfb
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


firefox_instance = {
    'xvfb_display': None,
    'driver': None,
}


def cleanup():
    """Must be called before exit"""
    global firefox_instance
    if firefox_instance['driver'] is not None:
        firefox_instance['driver'].quit()
    if firefox_instance['xvfb_display'] is not None:
        firefox_instance['xvfb_display'].stop()


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
    return '\n'.join([
        line
        for line in BeautifulSoup(html, "html.parser").stripped_strings
        if line
    ])


@contextmanager
def firefox():
    global firefox_instance
    if firefox_instance['xvfb_display'] is None:
        firefox_instance['xvfb_display'] = virtual_buffer()
    if firefox_instance['driver'] is None:
        firefox_instance['driver'] = webdriver.Firefox()
    yield firefox_instance['driver']


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
    exec(code, {'driver': driver})
