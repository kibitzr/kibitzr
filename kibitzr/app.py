import logging
import signal
import time
import code

import entrypoints

from .conf import settings, SettingsParser
from .fetcher import cleanup_fetchers, persistent_firefox
from .checker import Checker
from .bootstrap import create_boilerplate
from . import timeline


logger = logging.getLogger(__name__)


__all__ = [
    'Application',
]


class Application(object):

    def __init__(self):
        self.signals = {
            'reload_conf_pending': False,
            'interrupted': False,
            'open_backdoor': False,
            'orig': {
                signal.SIGINT: None,
                signal.SIGTERM: None,
                signal.SIGUSR1: None,
                signal.SIGUSR2: None,
            }
        }

    @staticmethod
    def bootstrap():
        create_boilerplate()

    def run(self, once=False, log_level=logging.INFO, names=None):
        # Reset global state for testability:
        self.signals.update({
            'reload_conf_pending': False,
            'interrupted': False,
            'open_backdoor': False,
        })
        self.setup_logger(log_level)
        self.connect_signals()
        try:
            while True:
                if self.signals['interrupted']:
                    return 1
                if self.signals['reload_conf_pending']:
                    settings().reread()
                    self.signals['reload_conf_pending'] = False
                checkers = Checker.create_from_settings(
                    checks=settings().checks,
                    names=names
                )
                if checkers:
                    self.before_start(checkers)
                    self.execute_all(checkers)
                    if once:
                        return 0
                    else:
                        self.check_forever(checkers)
                else:
                    logger.warning("No checks defined. Exiting")
                    return 1
        finally:
            cleanup_fetchers()
        return 0

    def disconnect_signals(self):
        signal.signal(signal.SIGINT, self.signals['orig'][signal.SIGINT])
        signal.signal(signal.SIGTERM, self.signals['orig'][signal.SIGTERM])
        try:
            signal.signal(signal.SIGUSR1, self.signals['orig'][signal.SIGUSR1])
            signal.signal(signal.SIGUSR2, self.signals['orig'][signal.SIGUSR2])
        except AttributeError:
            # Unavailable on Windows
            pass

    def connect_signals(self):
        self.signals['orig'][signal.SIGINT] = signal.signal(signal.SIGINT, self.on_interrupt)
        self.signals['orig'][signal.SIGTERM] = signal.signal(signal.SIGTERM, self.on_interrupt)
        try:
            self.signals['orig'][signal.SIGUSR1] = signal.signal(signal.SIGUSR1,
                                                                 self.on_reload_config)
            self.signals['orig'][signal.SIGUSR2] = signal.signal(signal.SIGUSR2, self.on_backdoor)
        except AttributeError:
            # Unavailable on Windows
            pass

    @staticmethod
    def execute_conf(conf):
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger('').handlers[0].level = logging.WARNING
        checks = SettingsParser().parse_checks(conf)
        for check in checks:
            Checker(check).check()

    def run_firefox(self):
        self.setup_logger(logging.INFO)
        persistent_firefox()

    @staticmethod
    def telegram_chat():
        from .notifier.telegram import chat_id
        chat_id()

    @staticmethod
    def setup_logger(log_level=logging.INFO):
        logging.getLogger("").setLevel(log_level)

    def check_forever(self, checkers):
        timeline.schedule_checks(checkers)
        logger.info("Starting infinite loop")
        while not self.signals['reload_conf_pending']:
            if self.signals['interrupted']:
                break
            if self.signals['open_backdoor']:
                self.signals['open_backdoor'] = False
                code.interact(
                    banner="Kibitzr debug shell",
                    local=locals(),
                )
            timeline.run_pending()
            if self.signals['interrupted']:
                break
            time.sleep(1)

    def execute_all(self, checkers):
        for checker in checkers:
            if not self.signals['interrupted']:
                checker.check()
            else:
                break

    def on_reload_config(self, *args, **kwargs):
        logger.info("Received SIGUSR1. Flagging configuration reload")
        self.signals['reload_conf_pending'] = True

    def on_backdoor(self, *args, **kwargs):
        logger.info("Received SIGUSR2. Flagging backdoor to open")
        self.signals['open_backdoor'] = True

    def on_interrupt(self, *args, **kwargs):
        if not self.signals['interrupted']:
            self.signals['interrupted'] = True
        else:
            # Third Ctrl+C to hard stop:
            self.disconnect_signals()

    def before_start(self, checkers):
        """
        Loads entry points named kibitzr.before_start
        and call each one with two arguments:

            1. Application instance;
            2. List of configured checkers
        """
        for point in entrypoints.get_group_all("kibitzr.before_start"):
            entry = point.load()
            entry(self, checkers)
