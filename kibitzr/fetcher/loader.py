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
        from .simple import requests_fetcher
        super(RequestsPromoter, self).__init__(conf)
        self.fetcher_func = requests_fetcher(conf)

    @classmethod
    def is_applicable(cls, conf):
        """Return whether this promoter is applicable for given conf"""
        return all((
            URLPromoter.is_applicable(conf),
            not cls.needs_firefox(conf),
        ))


class FirefoxPromoter(URLPromoter):

    PRIORITY = 15

    def __init__(self, conf):
        from .browser.fetcher import firefox_fetcher
        super(FirefoxPromoter, self).__init__(conf)
        self.fetcher_func = firefox_fetcher

    @classmethod
    def is_applicable(cls, conf):
        """Return whether this promoter is applicable for given conf"""
        return all((
            URLPromoter.is_applicable(conf),
            cls.needs_firefox(conf),
        ))


class ScriptPromoter(BasePromoter):

    PRIORITY = 15

    def __init__(self, conf):
        from .script import fetch_by_script
        super(ScriptPromoter, self).__init__(conf)
        self.fetcher_func = fetch_by_script

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
