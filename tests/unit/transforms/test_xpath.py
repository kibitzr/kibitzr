# -*- coding: utf-8 -*-
import pytest

from .helpers import run_transform, HTML


@pytest.mark.parametrize("selector,expected", [
    pytest.param('boolean(//body/h2/a)', 'True', id='boolean'),
    pytest.param("count(//div)", "2.0", id="float"),
    pytest.param("string(//a)", "Page", id="string"),
    pytest.param("//body/h2/a/@href", "page.html", id="attribute"),
    pytest.param(
        '//body/h2/a[@id="page-link"]',
        '<a href="page.html" id="page-link">Page</a>',
        id='element'
    ),
    pytest.param(
        '/html/namespace::*[name()]',
        'xml="http://www.w3.org/XML/1998/namespace"',
        id='namespace'
    ),
])
def test_xpath_selector(selector, expected):
    ok, content = run_transform('xpath', selector, HTML)
    assert ok is True
    assert content == expected


def test_xpath_selector_all():
    ok, content = run_transform('xpath-all', '//div', HTML)
    assert ok is True
    assert content == u'\n'.join([
        u'<div id="content"> Привет, Мир! </div>',
        u'<div class="footer"> Footer content </div>',
    ])
