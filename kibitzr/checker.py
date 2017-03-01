import functools
import logging
import traceback

from .fetcher import (
    firefox_fetcher,
    SessionFetcher,
    fetch_bash,
)
from .notifier import (
    SlackSession,
    post_bash,
    post_gitter,
    post_mailgun,
    post_python,
    post_smtp,
)
from .storage import report_changes
from .transformer import pipeline_factory


logger = logging.getLogger(__name__)


class Checker(object):
    def __init__(self, conf):
        self.conf = conf
        self.downloader = self.downloader_factory()
        self.report_error = self.error_reporter_factory()
        self.notifiers = self.create_notifiers()
        self.transform_pipeline = pipeline_factory(self.conf)

    @staticmethod
    def create_from_settings(pages):
        return [Checker(conf)
                for conf in pages]

    def check(self):
        ok, content = self.fetch()
        ok, report = self.transform(ok, content)
        if ok:
            self.notify(report=report)
        return ok, report

    def fetch(self):
        if self.is_script():
            logger.info("Fetching %r using bash script",
                        self.conf['name'])
        else:
            logger.info("Fetching %r at %r",
                        self.conf['name'], self.conf['url'])
        try:
            ok, content = self.downloader(self.conf)
        except Exception:
            logger.exception(
                "Exception occured while fetching page"
            )
            ok, content = False, traceback.format_exc()
        return ok, content

    def downloader_factory(self):
        if self.needs_firefox():
            return firefox_fetcher
        elif self.is_script():
            return fetch_bash
        else:
            return SessionFetcher(self.conf).fetch

    def is_script(self):
        return all((
            'url' not in self.conf,
            'script' in self.conf,
        ))

    def needs_firefox(self):
        return any(
            self.conf.get(key)
            for key in ('scenario', 'delay')
        )

    def transform(self, ok, content):
        ok, content = self.transform_pipeline(ok, content)
        if not ok:
            content = self.report_error(content)
        if content:
            content = content.strip()
        return ok, content

    def error_reporter_factory(self):
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
        if not notifiers_conf:
            logger.warning(
                "No notifications configured for %r",
                self.conf['name'],
            )
        return list(filter(None, [
            self.notifier_factory(notifier_conf)
            for notifier_conf in notifiers_conf
        ]))

    @staticmethod
    def notifier_factory(notifier_conf):
        try:
            key, value = next(iter(notifier_conf.items()))
        except AttributeError:
            key, value = notifier_conf, None
        if key == 'python':
            return functools.partial(post_python, code=value)
        elif key == 'bash':
            return functools.partial(post_bash, code=value)
        elif key == 'mailgun':
            return post_mailgun
        elif key == 'gitter':
            return post_gitter
        elif key == 'slack':
            return SlackSession().post
        elif key == 'smtp':
            return functools.partial(post_smtp, notifier_conf=value)
        else:
            logger.error("Unknown notifier %r", key)

    def notify(self, report, **kwargs):
        if report:
            logger.debug('Sending report: %r', report)
            for notifier in self.notifiers:
                try:
                    notifier(conf=self.conf, report=report)
                except Exception:
                    logger.exception(
                        "Exception occured during sending notification"
                    )
        else:
            logger.debug('Report is empty, skipping notification')
