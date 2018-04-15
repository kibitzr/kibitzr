"""
Kibitzr supports a number of fetchers and the list can be extended by plugins.

In the nutshell each fetcher takes conf and returns a tuple: ok, content.
where ok is boolean meaning success, and content is a Unicode string with fetch result.

Each fetcher has a promoter.
Promoter knows if the fetcher is applicable for given conf and
sets a priority for conflict resolution.

Promoter instance is initialized with conf and delegates calls to fetcher.
"""

import logging


logger = logging.getLogger(__name__)


def fetcher_factory(conf):
    """Return initialized fetcher capable of processing given conf."""
    applicable = []
    promoters = load_promoters()
    for promoter in promoters:
        if promoter.is_applicable(conf):
            applicable.append((promoter.PRIORITY, promoter))
    if applicable:
        best_match = sorted(applicable, reverse=True)[0][1]
        return best_match(conf)


def load_promoters():
    """Return list of available promoters"""
    # TODO: extend through entry_points
    return [
        RequestsPromoter,
        FirefoxPromoter,
        ScriptPromoter,
    ]


class BasePromoter(object):
    """
    Promoters are filtered by the result of is_applicable call,
    then sorted by PRIORITY.
    The one with highest PRIORITY is chosen for check.
    """

    PRIORITY = 10

    def __init__(self, conf):
        self.conf = conf
        self.fetcher_func = None  # To be overriden in descendants

    @staticmethod
    def is_applicable(conf):
        """Return whether this promoter is applicable for given conf"""
        return True

    def log_announcement(self):
        logger.info(u"Fetching %s using %s",
                    self.conf['name'],
                    self.__class__.__name__)

    def fetch(self):
        self.log_announcement()
        return self.fetcher_func(self.conf)
    __call__ = fetch


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
