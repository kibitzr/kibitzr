import logging

from .mailgun import post_mailgun
from .slack import post_slack
from .custom import post_python


logger = logging.getLogger(__name__)


def notify(conf, report):
    for rule in conf.get('notify', []):
        try:
            key, value = next(iter(rule.items()))
        except AttributeError:
            key, value = rule, None
        if key == 'slack':
            post_slack(value, report)
        elif key == 'python':
            post_python(value, report)
        elif key == 'mailgun':
            post_mailgun(conf, report)
