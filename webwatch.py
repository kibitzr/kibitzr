import os
import time
from contextlib import closing

import html2text
import sh
import yaml
from selenium import webdriver


def main():
    for page in read_pages():
        content = download_page(page)
        with open(os.path.join('pages', page['name']), 'w') as fp:
            fp.write(content)
    if save_changes():
        print(report_diff())


def download_page(conf):
    with closing(webdriver.Firefox()) as driver:
        driver.get(conf['url'])
        if conf.get('delay'):
            time.sleep(conf['delay'])
        tag_name = conf.get('tag')
        if tag_name:
            elem = driver.find_element_by_tag_name(tag_name)
            html = elem.get_attribute('outerHTML')
        else:
            xpath = conf.get('xpath', '//*')
            elem = driver.find_element_by_xpath(xpath)
            html = elem.get_attribute('outerHTML')
        output_format = conf.get('format', 'html')
        if output_format == 'text':
            return sanitize(html)
        elif output_format == 'html':
            return html


def sanitize(html):
    return html2text.html2text(html)


def read_pages():
    with open('watch.yml') as fp:
        conf = yaml.load(fp)
    return conf['pages']


def save_changes():
    sh.git('add', '-A', 'pages')
    sh.git.commit('-m', 'Web watch')


def report_diff():
    return sh.git.log('-1', '-p')


if __name__ == '__main__':
    main()
