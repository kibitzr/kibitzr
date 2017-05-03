import logging
import traceback

from .browser import (
    needs_firefox,
    firefox_fetcher,
)
from .simple import requests_fetcher
from .script import fetch_by_script


logger = logging.getLogger(__name__)


def fetcher_factory(conf):
    if needs_firefox(conf):
        return URLFetcher(conf, firefox_fetcher)
    elif is_script(conf):
        return ScriptFetcher(conf, fetch_by_script)
    else:
        return URLFetcher(conf, requests_fetcher(conf))


class URLFetcher(object):

    def __init__(self, conf, fetcher_func):
        self.conf = conf
        self.fetcher_func = fetcher_func

    def fetch(self):
        self.log_announcement()
        try:
            ok, content = self.fetcher_func(self.conf)
        except:
            logger.exception(
                "Exception occured while fetching check"
            )
            ok, content = False, traceback.format_exc()
        return ok, content
    __call__ = fetch

    def log_announcement(self):
        logger.info("Fetching %r at %r",
                    self.conf['name'], self.conf['url'])


class ScriptFetcher(URLFetcher):

    def log_announcement(self):
        logger.info("Fetching %r using script",
                    self.conf['name'])


def is_script(conf):
    return all((
        'url' not in conf,
        'script' in conf,
    ))
