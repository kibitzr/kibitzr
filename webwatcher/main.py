#!/usr/bin/env python
import functools
import time
from xmlrpc.client import ServerProxy

import schedule

from .fetcher import fetch
from .storage import report_changes
from .settings import PAGES
from .mailgun import post_mailgun


def main():
    check_all_pages(PAGES)
    schedule_checks(PAGES)
    while True:
        schedule.run_pending()
        time.sleep(60)


def schedule_checks(page_confs):
    for conf in page_confs:
        period = conf.get('period', 300)
        schedule.every(period).seconds.do(
            functools.partial(check_page, conf)
        )


def check_all_pages(page_confs):
    for conf in page_confs:
        check_page(conf)


def check_page(conf):
    content = fetch(conf)
    report = report_changes(conf, content)
    if report:
        notify(conf, report)


def notify(conf, report):
    for rule in conf.get('notify', []):
        try:
            key, value = next(iter(rule.items()))
        except AttributeError:
            key, value = rule, None
        if key == 'slack':
            post_slack(value, report)
        if key == 'mailgun':
            post_mailgun(conf, report)


def post_slack(channel, text):
    s = ServerProxy('http://localhost:34278', allow_none=True)
    s.post(channel, text)
