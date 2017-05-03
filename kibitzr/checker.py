import logging

from .fetcher import fetcher_factory
from .notifier import notify_factory
from .transformer import transform_factory


logger = logging.getLogger(__name__)


class Checker(object):
    def __init__(self, conf):
        self.conf = conf
        self.fetch = fetcher_factory(conf)
        self.transform = transform_factory(self.conf)
        self.notify = notify_factory(self.conf)

    @classmethod
    def create_from_settings(cls, checks, names=None):
        if names:
            selected_checks = [
                conf
                for conf in checks
                if conf['name'] in names
            ]
            selected_names = [conf['name'] for conf in selected_checks]
            if len(selected_checks) < len(checks):
                logger.info("Filtered list of checks to: %r",
                            ", ".join(sorted(selected_names)))
                checks = selected_checks
            if len(selected_names) < len(names):
                logger.error(
                    "Following check(s) were not found: %r",
                    ", ".join(sorted(set(names).difference(selected_names)))
                )
        return [cls(conf)
                for conf in checks]

    def check(self):
        ok, content = self.fetch()
        ok, report = self.transform(ok, content)
        self.notify(report=report)
        return ok, report
