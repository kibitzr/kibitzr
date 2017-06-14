import logging


logger = logging.getLogger(__name__)


def fetcher_factory(conf):
    if needs_firefox(conf):
        from .browser.fetcher import firefox_fetcher
        return URLFetcher(conf, firefox_fetcher)
    elif is_script(conf):
        from .script import fetch_by_script
        return ScriptFetcher(conf, fetch_by_script)
    else:
        from .simple import requests_fetcher
        return URLFetcher(conf, requests_fetcher(conf))


class URLFetcher(object):

    def __init__(self, conf, fetcher_func):
        self.conf = conf
        self.fetcher_func = fetcher_func

    def fetch(self):
        self.log_announcement()
        ok, content = self.fetcher_func(self.conf)
        return ok, content
    __call__ = fetch

    def log_announcement(self):
        logger.info(u"Fetching %s at %s",
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


def needs_firefox(conf):
    return any(
        conf.get(key)
        for key in ('delay', 'scenario', 'form')
    )
