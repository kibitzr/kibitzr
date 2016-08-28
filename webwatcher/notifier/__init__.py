import logging

from .mailgun import post_mailgun
from .custom import post_python


logger = logging.getLogger(__name__)


def notify(conf, report):
    for rule in conf.get('notify', []):
        try:
            key, value = next(iter(rule.items()))
        except AttributeError:
            key, value = rule, None
        try:
            if key == 'python':
                post_python(value, report)
            elif key == 'mailgun':
                post_mailgun(conf, report)
            else:
                logger.error("Unknown notifier %r", rule)
        except Exception:
            logger.exception(
                "Exception occured during sending notification"
            )
