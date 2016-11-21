import logging
import signal
import time
import code

import schedule

from .conf import settings
from .fetcher import cleanup_fetchers
from .checker import Checker


logger = logging.getLogger(__name__)
reload_conf_pending = False
interrupted = False
open_backdoor = False


def main(once=False, log_level=logging.INFO):
    global reload_conf_pending, interrupted
    logging.getLogger("").setLevel(log_level)
    logger.debug("Arguments: %r",
                 {"once": once, "log_level": log_level})
    signal.signal(signal.SIGUSR1, on_reload_config)
    signal.signal(signal.SIGUSR2, on_backdoor)
    signal.signal(signal.SIGINT, on_interrupt)
    try:
        while True:
            if interrupted:
                break
            if reload_conf_pending:
                settings().reread()
                reload_conf_pending = False
            checkers = Checker.create_from_settings(settings().pages)
            check_all_pages(checkers)
            if once or interrupted:
                break
            else:
                check_forever(checkers)
    finally:
        cleanup_fetchers()


def check_forever(checkers):
    global reload_conf_pending, interrupted, open_backdoor
    schedule_checks(checkers)
    logger.info("Starting infinite loop")
    while not reload_conf_pending:
        if interrupted:
            break
        if open_backdoor:
            open_backdoor = False
            console = code.interact(banner="Kibitzr debug shell", local=locals())
        schedule.run_pending()
        if interrupted:
            break
        time.sleep(1)


def schedule_checks(checkers):
    schedule.clear()
    for checker in checkers:
        conf = checker.conf
        period = conf.get("period", 300)
        logger.info(
            "Scheduling checks for %r every %r seconds",
            conf["name"],
            period,
        )
        schedule.every(period).seconds.do(checker.check)


def check_all_pages(checkers):
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
