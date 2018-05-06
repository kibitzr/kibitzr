import logging


logger = logging.getLogger(__name__)


class BasePromoter(object):
    """
    Promoters are filtered by the result of is_applicable call,
    then sorted by PRIORITY.
    The one with highest PRIORITY is chosen for check.
    """

    PRIORITY = 10

    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def is_applicable(conf):
        """Return whether this promoter is applicable for given conf"""
        return bool(conf)

    def log_announcement(self):
        logger.info(u"Fetching %s using %s",
                    self.conf['name'],
                    self.__class__.__name__)

    def fetch(self):
        self.log_announcement()

    def __call__(self):
        return self.fetch()
