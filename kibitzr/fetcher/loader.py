import logging
import entrypoints

from .base import BasePromoter


logger = logging.getLogger(__name__)


def load_promoters():
    """Return list of available promoters"""
    builtins = [
        RequestsPromoter,
        FirefoxPromoter,
        ScriptPromoter,
    ]
    return builtins + load_extensions()


def load_extensions():
    """Return list of fetcher promoters defined in Kibitzr extensions"""
    return [
        point.load()
        for point in entrypoints.get_group_all("kibitzr.fetcher")
    ]


class URLPromoter(BasePromoter):

    @staticmethod
    def is_applicable(conf):
        """Return whether this promoter is applicable for given conf"""
        return bool(conf.get('url'))

    def log_announcement(self):
        logger.info(u"Fetching %s at %s",
                    self.conf['name'], self.conf['url'])

    @staticmethod
    def needs_firefox(conf):
        return any(
            conf.get(key)
            for key in ('delay', 'scenario', 'form')
        )


class RequestsPromoter(URLPromoter):

    PRIORITY = 5  # default fallback

    def __init__(self, conf):
        super(RequestsPromoter, self).__init__(conf)
        self._fetcher = None

    @classmethod
    def is_applicable(cls, conf):
        """Return whether this promoter is applicable for given conf"""
        return all((
            URLPromoter.is_applicable(conf),
            not cls.needs_firefox(conf),
        ))

    def fetch(self):
        from .simple import requests_fetcher
        super(RequestsPromoter, self).fetch()
        if not self._fetcher:
            self._fetcher = requests_fetcher(self.conf)
        return self._fetcher()


class FirefoxPromoter(URLPromoter):

    PRIORITY = 15

    @classmethod
    def is_applicable(cls, conf):
        """Return whether this promoter is applicable for given conf"""
        return all((
            URLPromoter.is_applicable(conf),
            cls.needs_firefox(conf),
        ))

    def fetch(self):
        from .browser.fetcher import firefox_fetcher
        super(FirefoxPromoter, self).fetch()
        return firefox_fetcher(self.conf)


class ScriptPromoter(BasePromoter):

    PRIORITY = 15

    @staticmethod
    def is_applicable(conf):
        """Return whether this promoter is applicable for given conf"""
        return all((
            'url' not in conf,
            'script' in conf,
        ))

    def log_announcement(self):
        logger.info("Fetching %r using script",
                    self.conf['name'])

    def fetch(self):
        from .script import fetch_by_script
        super(ScriptPromoter, self).fetch()
        return fetch_by_script(self.conf)
