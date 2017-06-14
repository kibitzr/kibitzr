"""
FireFox housekeeping - starting and stopping process
"""

import os
import sys
import shutil
import logging
from contextlib import contextmanager


PROFILE_DIR = 'firefox_profile'
logger = logging.getLogger(__name__)
FIREFOX_INSTANCE = {
    'xvfb_display': None,
    'driver': None,
    'headed_driver': None,
}


def cleanup():
    """Must be called before exit"""
    temp_dirs = []
    if FIREFOX_INSTANCE['driver'] is not None:
        if FIREFOX_INSTANCE['driver'].profile:
            temp_dirs.append(FIREFOX_INSTANCE['driver'].profile.profile_dir)
        try:
            FIREFOX_INSTANCE['driver'].quit()
            FIREFOX_INSTANCE['driver'] = None
        except:
            logger.exception(
                "Exception occurred in browser cleanup"
            )
    if FIREFOX_INSTANCE['headed_driver'] is not None:
        if FIREFOX_INSTANCE['headed_driver'].profile:
            temp_dirs.append(FIREFOX_INSTANCE['headed_driver'].profile.profile_dir)
        try:
            FIREFOX_INSTANCE['headed_driver'].quit()
            FIREFOX_INSTANCE['headed_driver'] = None
        except:
            logger.exception(
                "Exception occurred in browser cleanup"
            )
    if FIREFOX_INSTANCE['xvfb_display'] is not None:
        FIREFOX_INSTANCE['xvfb_display'].stop()
        FIREFOX_INSTANCE['xvfb_display'] = None
    for temp_dir in temp_dirs:
        shutil.rmtree(temp_dir, ignore_errors=True)


@contextmanager
def firefox(headless=True):
    """
    Context manager returning Selenium webdriver.
    Instance is reused and must be cleaned up on exit.
    """
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    if headless:
        if FIREFOX_INSTANCE['xvfb_display'] is None:
            FIREFOX_INSTANCE['xvfb_display'] = virtual_buffer()
        driver_key = 'driver'
    else:
        driver_key = 'headed_driver'
    if FIREFOX_INSTANCE[driver_key] is None:
        if logger.level == logging.DEBUG:
            firefox_binary = FirefoxBinary(log_file=sys.stdout)
        else:
            firefox_binary = None
        # Load profile, if it exists:
        if os.path.isdir(PROFILE_DIR):
            firefox_profile = webdriver.FirefoxProfile(PROFILE_DIR)
        else:
            firefox_profile = None
        FIREFOX_INSTANCE[driver_key] = webdriver.Firefox(
            firefox_binary=firefox_binary,
            firefox_profile=firefox_profile,
        )
    yield FIREFOX_INSTANCE[driver_key]


def virtual_buffer():
    """
    Try to start xvfb, trying multiple (up to 5) times if a failure
    """
    from xvfbwrapper import Xvfb
    for _ in range(0, 6):
        xvfb_display = Xvfb()
        xvfb_display.start()
        # If Xvfb started, return.
        if xvfb_display.proc is not None:
            return xvfb_display
    raise Exception("Xvfb could not be started after six attempts.")
