#!/usr/bin/env python
import json
import os
import time
from contextlib import closing, contextmanager
import functools

import html2text
import requests
import schedule
import sh
import yaml
from selenium import webdriver
from xmlrpc.client import ServerProxy
from xvfbwrapper import Xvfb


git = sh.git.bake('--no-pager', _cwd="pages")


def main():
    conf = pages_conf()
    check_all_pages(conf)
    schedule_checks(conf)
    while True:
        schedule.run_pending()
        time.sleep(60)


def schedule_checks(confs):
    for conf in confs:
        period = conf.get('period', 300)
        schedule.every(period).seconds.do(functools.partial(check_page, conf))


def check_all_pages(confs):
    for conf in confs:
        check_page(conf)


def check_page(conf):
    save_page(conf, download_page(conf))
    if save_changes():
        report = report_diff()
        notify(conf, report)


def download_page(conf):
    url = conf['url']
    output_format = conf.get('format', 'html')
    if output_format in ('asis', 'json'):
        response = requests.get(url)
        if output_format == 'json':
            return json.dumps(response.json, indent=True)
        else:
            return response.text
    else:
        delay = conf.get('delay')
        tag_name = conf.get('tag')
        xpath = conf.get('xpath', '//*')
        with firefox() as browser:
            browser.get(url)
            if delay:
                time.sleep(delay)
            if tag_name:
                elem = browser.find_element_by_tag_name(tag_name)
                html = elem.get_attribute('outerHTML')
            else:
                elem = browser.find_element_by_xpath(xpath)
                html = elem.get_attribute('outerHTML')
            if output_format == 'text':
                return sanitize(html)
            elif output_format == 'html':
                return html


def save_page(conf, content):
    with open(os.path.join('pages', conf['name']), 'w') as fp:
        fp.write(content)


def sanitize(html):
    return html2text.html2text(html)


def pages_conf():
    with open('watch.yml') as fp:
        conf = yaml.load(fp)
    return conf['pages']


def notify_conf():
    with open('watch.yml') as fp:
        conf = yaml.load(fp)
    return conf['on_change']


def save_changes():
    git('add', '-A', '.')
    try:
        git.commit('-m', 'Web watch')
        return True
    except sh.ErrorReturnCode_1:
        return False


def report_diff():
    return git.log('-1', '-p', '--no-color').stdout


def notify(conf, report):
    for rule in notify_conf():
        for key, value in rule.items():
            if key == 'slack':
                post_slack(value, report)


def post_slack(channel, text):
    s = ServerProxy('http://localhost:34278', allow_none=True)
    s.post(channel, text)


@contextmanager
def virtual_buffer():
    """
    Try to start xvfb, trying multiple (up to 5) times if a failure
    """
    for i in range(0, 6):
        xvfb_display = Xvfb()
        xvfb_display.start()
        # If Xvfb started, return.
        if xvfb_display.proc is not None:
            try:
                yield
                return
            finally:
                xvfb_display.stop()
    raise Exception("Xvfb could not be started after six attempts.")


@contextmanager
def firefox():
    with virtual_buffer():
        with closing(webdriver.Firefox()) as driver:
            yield driver


if __name__ == '__main__':
    main()
