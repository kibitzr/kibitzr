import logging
import signal
import time
import code

import schedule

from .conf import settings, SettingsParser
from .fetcher import cleanup_fetchers, persistent_firefox
from .checker import Checker
from .bootstrap import create_boilerplate


logger = logging.getLogger(__name__)
reload_conf_pending = False
interrupted = False
open_backdoor = False


__all__ = [
    'main',
    'run_firefox',
    'execute_conf',
    'create_boilerplate',
    'telegram_chat',
]


def bootstrap():
    create_boilerplate()


def main(once=False, log_level=logging.INFO, names=None):
    global reload_conf_pending, interrupted, open_backdoor
    # Reset global state for testability:
    reload_conf_pending, interrupted, open_backdoor = False, False, False
    setup_logger(log_level)
    connect_signals()
    try:
        while True:
            if interrupted:
                break
            if reload_conf_pending:
                settings().reread()
                reload_conf_pending = False
            checkers = Checker.create_from_settings(
                checks=settings().checks,
                names=names
            )
            if checkers:
                execute_all(checkers)
                if once or interrupted:
                    break
                else:
                    check_forever(checkers)
            else:
                logger.warning("No checks defined. Exiting")
                return 1
    finally:
        cleanup_fetchers()
    return 0


def connect_signals():
    signal.signal(signal.SIGINT, on_interrupt)
    signal.signal(signal.SIGTERM, on_interrupt)
    try:
        signal.signal(signal.SIGUSR1, on_reload_config)
        signal.signal(signal.SIGUSR2, on_backdoor)
    except AttributeError:
        # Unavailable on Windows
        pass


def execute_conf(conf):
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('').handlers[0].level = logging.WARNING
    checks = SettingsParser().parse_checks(conf)
    for check in checks:
        Checker(check).check()


def run_firefox():
    setup_logger(logging.DEBUG)
    persistent_firefox()


def telegram_chat():
    from .notifier.telegram import chat_id
    chat_id()


def setup_logger(log_level=logging.INFO):
    logging.getLogger("").setLevel(log_level)


def check_forever(checkers):
    global reload_conf_pending, interrupted, open_backdoor
    schedule_checks(checkers)
    logger.info("Starting infinite loop")
    while not reload_conf_pending:
        if interrupted:
            break
        if open_backdoor:
            open_backdoor = False
            code.interact(
                banner="Kibitzr debug shell",
                local=locals(),
            )
        schedule.run_pending()
        if interrupted:
            break
        time.sleep(1)


def schedule_checks(checkers):
    schedule.clear()
    for checker in checkers:
        conf = checker.conf
        period = conf["period"]
        logger.info(
            "Scheduling checks for %r every %r seconds",
            conf["name"],
            period,
        )
        schedule.every(period).seconds.do(checker.check)


def execute_all(checkers):
    global interrupted
    for checker in checkers:
        if not interrupted:
            checker.check()


def on_reload_config(*args, **kwargs):
    global reload_conf_pending
    logger.info("Received SIGUSR1. Flagging configuration reload")
    reload_conf_pending = True


def on_backdoor(*args, **kwargs):
    global open_backdoor
    logger.info("Received SIGUSR2. Flagging backdoor to open")
    open_backdoor = True


def on_interrupt(*args, **kwargs):
    global interrupted
    interrupted = True
