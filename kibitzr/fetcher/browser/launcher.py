"""
FireFox housekeeping - starting and stopping process
"""

import os
import shutil
import logging
from contextlib import contextmanager


PROFILE_DIR = 'firefox_profile'
logger = logging.getLogger(__name__)
FIREFOX_INSTANCE = {
    'headless': None,
    'headed': None,
}


def cleanup():
    """Must be called before exit"""
    temp_dirs = []
    for key in ('headless', 'headed'):
        if FIREFOX_INSTANCE[key] is not None:
            if FIREFOX_INSTANCE[key]['profile']:
                temp_dirs.append(FIREFOX_INSTANCE[key]['profile'].path)
            try:
                FIREFOX_INSTANCE[key]['webdriver'].quit()
                FIREFOX_INSTANCE[key] = None
            except:
                logger.exception(
                    "Exception occurred in browser cleanup"
                )
    for temp_dir in temp_dirs:
        shutil.rmtree(temp_dir, ignore_errors=True)


@contextmanager
def firefox(headless=True):
    """
    Context manager returning Selenium webdriver.
    Instance is reused and must be cleaned up on exit.
    """
    from selenium import webdriver  # pylint: disable=import-outside-toplevel
    from selenium.webdriver.firefox.options import Options  # pylint: disable=import-outside-toplevel
    firefox_options = Options()
    if headless:
        driver_key = 'headless'
        firefox_options.add_argument('-headless')
    else:
        driver_key = 'headed'
    # Load profile, if it exists:
    if os.path.isdir(PROFILE_DIR):
        firefox_profile = webdriver.FirefoxProfile(PROFILE_DIR)
        firefox_options.profile = firefox_profile
    else:
        firefox_profile = None
    if FIREFOX_INSTANCE[driver_key] is None:
        FIREFOX_INSTANCE[driver_key] = {
            'webdriver': webdriver.Firefox(options=firefox_options),
            'profile': firefox_profile
        }
    yield FIREFOX_INSTANCE[driver_key]['webdriver']
