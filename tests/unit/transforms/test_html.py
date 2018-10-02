# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from kibitzr.transformer import transform_factory


def run_transform(key, value, content):
    pipeline = transform_factory({'transform': [{key: value}]})
    return pipeline(True, content)


def test_tag_selector():
    ok, content = run_transform('tag', 'a', HTML)
    assert ok is True
    assert content == '<a href="page.html" id="page-link">Page</a>'


def test_css_selector():
    ok, content = run_transform('css', 'body h2.nav a#page-link', HTML)
    assert ok is True
    assert content == '<a href="page.html" id="page-link">Page</a>'


def test_css_selector_all():
    ok, content = run_transform('css-all', 'div', HTML)
    assert ok is True
    assert prettify(content) == u'\n'.join([
        u'<div id="content">',
        u' Привет, Мир!',
        u'</div>',
        u'',
        u'<div class="footer">',
        u' Footer content',
        u'</div>',
    ])


def test_xpath_selector():
    ok, content = run_transform('xpath', '//body/h2/a[@id="page-link"]', HTML)
    assert ok is True
    assert content == '<a href="page.html" id="page-link">Page</a>'


def test_xpath_selector_all():
    ok, content = run_transform('xpath-all', '//div', HTML)
    assert ok is True
    assert content == u'\n'.join([
        u'<div id="content"> Привет, Мир! </div>',
        u'<div class="footer"> Footer content </div>',
    ])


def test_xpath_selector_boolean():
    ok, content = run_transform('xpath', 'boolean(//body/h2/a)', HTML)
    assert ok is True
    assert content == 'True'


def test_xpath_selector_float():
    ok, content = run_transform('xpath', 'count(//div)', HTML)
    assert ok is True
    assert content == '2.0'


def test_xpath_selector_attribute():
    ok, content = run_transform('xpath', '//body/h2/a/@href', HTML)
    assert ok is True
    assert content == 'page.html'


def test_xpath_selector_namespace():
    ok, content = run_transform('xpath', '/html/namespace::*[name()]', HTML)
    assert ok is True
    assert content == 'xml="http://www.w3.org/XML/1998/namespace"'


def test_extract_test():
    ok, content = run_transform('text', None, HTML)
    assert ok is True
    assert content.strip() == u"\n".join([
        u"Page",
        u"Привет, Мир!",
        u"Footer content",
    ])


HTML = u"""<?xml version="1.0" encoding="utf-8"?>
<html>
    <body>
        <h2 class="header nav">
            <a href="page.html" id="page-link">Page</a>
        </h2>
        <div id="content">
            Привет, Мир!
        </div>
        <div class="footer">
            Footer content
        </div>
    </body>
</html>
"""


def prettify(html):
    return "\n".join(
        child.prettify()
        for child in BeautifulSoup(html, "lxml").html.body.children
    )
