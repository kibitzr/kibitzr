# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from .helpers import run_transform, HTML


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


def test_extract_test():
    ok, content = run_transform('text', None, HTML)
    assert ok is True
    assert content.strip() == u"\n".join([
        u"Page",
        u"Привет, Мир!",
        u"Footer content",
    ])


def prettify(html):
    return "\n".join(
        child.prettify()
        for child in BeautifulSoup(html, "lxml").html.body.children
    )
