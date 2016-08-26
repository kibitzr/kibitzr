#!/usr/bin/env python

import os
import time
from contextlib import closing, contextmanager
from xmlrpc.client import ServerProxy

import html2text
import sh
import yaml
from selenium import webdriver
from xvfbwrapper import Xvfb
import schedule


git = sh.git.bake('--no-pager', _cwd="pages")


def main():
    check_pages()
    schedule.every(5).minutes.do(check_pages)
    while True:
        schedule.run_pending()
        time.sleep(60)


def check_pages():
    for conf in pages_conf():
        save_page(conf, download_page(conf))
    if save_changes():
        report = report_diff()
        notify(report)


def download_page(conf):
    with firefox() as browser:
        browser.get(conf['url'])
        if conf.get('delay'):
            time.sleep(conf['delay'])
        tag_name = conf.get('tag')
        if tag_name:
            elem = browser.find_element_by_tag_name(tag_name)
            html = elem.get_attribute('outerHTML')
        else:
            xpath = conf.get('xpath', '//*')
            elem = browser.find_element_by_xpath(xpath)
            html = elem.get_attribute('outerHTML')
        output_format = conf.get('format', 'html')
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


def notify(report):
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
