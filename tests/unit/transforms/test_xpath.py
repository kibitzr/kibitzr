# -*- coding: utf-8 -*-
from .helpers import run_transform, HTML


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
