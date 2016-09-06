import logging
import signal
import time

import schedule

from .conf import settings
from .fetcher import fetch, cleanup_fetchers
from .notifier import notify
from .storage import report_changes


logger = logging.getLogger(__name__)
reload_conf_pending = False
interrupted = False


def main(once=False, log_level=logging.INFO):
    global reload_conf_pending, interrupted
    logging.getLogger("").setLevel(log_level)
    logger.debug("Arguments: %r",
                 {"once": once, "log_level": log_level})
    signal.signal(signal.SIGUSR1, on_reload_config)
    signal.signal(signal.SIGINT, on_interrupt)
    try:
        while True:
            if interrupted:
                break
            if reload_conf_pending:
                settings().reread()
                reload_conf_pending = False
            logger.debug("Configration: %r", settings.pages)
            check_all_pages(settings().pages)
            if once or interrupted:
                break
            else:
                schedule_checks(settings().pages)
                logger.info("Starting infinite loop")
                while not reload_conf_pending:
                    if interrupted:
                        break
                    schedule.run_pending()
                    if interrupted:
                        break
                    time.sleep(1)
    finally:
        cleanup_fetchers()


def schedule_checks(page_confs):
    schedule.clear()
    for conf in page_confs:
        period = conf.get("period", 300)
        logger.info(
            "Scheduling checks for %r every %r seconds",
            conf["name"],
            period,
        )
        schedule.every(period).seconds.do(
            lambda conf=conf: check_page(conf)
        )


def check_all_pages(page_confs):
    global interrupted
    for conf in page_confs:
        if not interrupted:
            check_page(conf)


def check_page(conf):
    global interrupted
    logger.info("Checking %r at %r", conf['name'], conf['url'])
    ok, content = fetch(conf)
    if not interrupted:
        report = make_report(conf, ok, content)
        if report:
            notify(conf, report)


def make_report(conf, ok, content):
    if ok:
        return report_changes(conf, content)
    else:
        error_policy = conf.get('error', 'notify')
        if error_policy == 'notify':
            return content
        elif error_policy == 'ignore':
            return None
        else:  # output
            return report_changes(conf, content)


def on_reload_config(signum, stack):
    global reload_conf_pending
    logger.info("Received SIGUSR1. Flagging configuration reload")
    reload_conf_pending = True


def on_interrupt(signum, stack):
    global interrupted
    interrupted = True
