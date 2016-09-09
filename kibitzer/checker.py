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
        ok, content = self.fetch()
        report = self.make_report(ok, content)
        if report:
            for notifier in self.notifiers:
                self.notify(notifier, ok, report)

    def fetch(self):
        logger.info("Fetching %r at %r",
                    self.conf['name'], self.conf['url'])
        try:
            ok, content = self.downloader(self.conf)
        except Exception:
            logger.exception(
                "Exception occured while fetching page"
            )
            ok, content = None, traceback.format_exc()
        return ok, content

    def choose_downloader(self):
        if self.needs_firefox():
            return firefox_fetcher
        else:
            return simple_fetcher

    def needs_firefox(self):
        return any(
            self.conf.get(key)
            for key in ('scenario', 'delay', 'xpath', 'tag')
        )

    def make_report(self, ok, content):
        if ok:
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

    def notify(self, notifier, ok, report):
        try:
            notifier(
                conf=self.conf,
                ok=ok,
                report=report,
            )
        except Exception:
            logger.exception(
                "Exception occured during sending notification"
            )
