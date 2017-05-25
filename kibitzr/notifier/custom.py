import logging

from kibitzr.stash import LazyStash
from ..conf import settings


logger = logging.getLogger(__name__)
NAME = 'python'


class PythonNotify(object):

    def __init__(self, conf, value):
        self.code = value
        self.context = {
            'conf': conf,
            'creds': settings().creds,
        }

    def __call__(self, report):
        context = dict(
            self.context,
            text=report,  # legacy
            content=report,
            stash=LazyStash(),
        )
        logger.info("Executing Python notifier")
        logger.debug(self.code)
        exec(self.code, context)


def notify_factory(conf, value):
    return PythonNotify(conf, value)
