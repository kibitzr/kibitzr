import functools
import logging
import traceback

from .fetcher import firefox_fetcher, simple_fetcher
from .storage import report_changes
from .notifier import post_mailgun, post_python, post_bash


logger = logging.getLogger(__name__)


class Checker(object):
    def __init__(self, conf):
        self.conf = conf
        self.downloader = self.choose_downloader()
        self.report_error = self.choose_error_reporter()
        self.notifiers = self.create_notifiers()

    @staticmethod
    def create_from_settings(pages):
        return [Checker(conf)
                for conf in pages]

    def check(self):
        status_code, content = self.fetch()
        report = self.make_report(status_code, content)
        for notifier in self.notifiers:
            self.notify(notifier, status_code, report)

    def fetch(self):
        logger.info("Fetching %r at %r",
                    self.conf['name'], self.conf['url'])
        try:
            status_code, content = self.downloader(self.conf)
        except Exception:
            logger.exception(
                "Exception occured while fetching page"
            )
            status_code, content = None, traceback.format_exc()
        return status_code, content

    def choose_downloader(self):
        if self.conf.get('scenario'):
            return firefox_fetcher
        else:
            return simple_fetcher

    def make_report(self, status_code, content):
        if self.http_ok(status_code):
            return self.persistent_changes(content)
        else:
            return self.report_error(content)

    def choose_error_reporter(self):
        error_policy = self.conf.get('error', 'notify')
        if error_policy == 'notify':
            return self.noop
        elif error_policy == 'ignore':
            return self.mute
        else:  # output
            return self.persistent_changes

    @staticmethod
    def http_ok(status_code):
        return (status_code is not None) and (200 <= status_code < 300)

    def persistent_changes(self, content):
        return report_changes(self.conf, content)

    @staticmethod
    def noop(content):
        return content

    @staticmethod
    def mute(content):
        return None

    def create_notifiers(self):
        notifiers_conf = self.conf.get('notify', [])
        if notifiers_conf:
            logger.info(
                "Sending notification for %r",
                self.conf["name"],
            )
        else:
            logger.warning(
                "No notifications configured for %r",
                self.conf['name'],
            )
        result = []
        for notifier in notifiers_conf:
            try:
                key, value = next(iter(notifier.items()))
            except AttributeError:
                key, value = notifier, None
            if key == 'python':
                result.append(functools.partial(post_python, code=value))
            elif key == 'bash':
                result.append(functools.partial(post_bash, code=value))
            elif key == 'mailgun':
                result.append(post_mailgun)
            else:
                logger.error("Unknown notifier %r", key)
        return result

    def notify(self, notifier, status_code, report):
        try:
            notifier(
                conf=self.conf,
                status_code=status_code,
                report=report,
            )
        except Exception:
            logger.exception(
                "Exception occured during sending notification"
            )
