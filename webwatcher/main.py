import functools
import time
import logging

import schedule

from .fetcher import fetch, cleanup_fetchers
from .storage import report_changes
from .notifier import notify
from .conf import settings


logger = logging.getLogger(__name__)


def main(once=False, log_level=logging.INFO):
    logging.getLogger("").setLevel(log_level)
    logger.debug("Arguments: %r",
                 {"once": once, "log_level": log_level})
    logger.debug("Configration: %r", settings.pages)
    try:
        check_all_pages(settings.pages)
        if not once:
            schedule_checks(settings.pages)
            logger.info("Starting infinite loop")
            while True:
                schedule.run_pending()
                time.sleep(60)
    finally:
        cleanup_fetchers()


def schedule_checks(page_confs):
    for conf in page_confs:
        period = conf.get("period", 300)
        logger.info(
            "Scheduling checks for %r every %r seconds",
            conf["name"],
            period,
        )
        schedule.every(period).seconds.do(
            functools.partial(check_page, conf)
        )


def check_all_pages(page_confs):
    for conf in page_confs:
        check_page(conf)


def check_page(conf):
    logger.info("Checking %r at %r", conf['name'], conf['url'])
    ok, content = fetch(conf)
    if ok:
        report = report_changes(conf, content)
    else:
        error_policy = conf.get('error', 'notify')
        if error_policy == 'notify':
            report = content
        elif error_policy == 'ignore':
            report = None
        else:  # output
            report = report_changes(conf, content)
    if report:
        logger.info("Sending notification for %r", conf["name"])
        notify(conf, report)
