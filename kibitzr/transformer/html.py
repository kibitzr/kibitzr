import sys
import contextlib
import logging

import six
from lxml import etree
from bs4 import BeautifulSoup

from .utils import wrap_dummy, bake_parametrized


logger = logging.getLogger(__name__)


def tag_selector(selector, html):
    with deep_recursion():
        soup = BeautifulSoup(html, "html.parser")
        element = soup.find(selector)
        if element:
            return True, six.text_type(element)
        else:
            logger.warning('Tag not found: %r', selector)
            return False, html


def css_selector(selector, html, select_all=False):
    with deep_recursion():
        soup = BeautifulSoup(html, "html.parser")
        try:
            elements = soup.select(selector)
            if select_all:
                result = u"".join(six.text_type(x)
                                  for x in elements)
            else:
                result = six.text_type(elements[0])
            return True, result
        except IndexError:
            logger.warning('CSS selector not found: %r', selector)
            return False, html


def xpath_selector(selector, html):
    root = etree.fromstring(html, parser=etree.HTMLParser())
    elements = root.xpath(selector)
    if elements:
        return True, etree.tostring(
            next(iter(elements)),
            method='html',
            pretty_print=True,
            encoding='unicode',
        )
    else:
        logger.warning('XPath selector not found: %r', selector)
        return False, html


def extract_text(html):
    with deep_recursion():
        strings = BeautifulSoup(html, "html.parser").stripped_strings
        return True, u'\n'.join([
            line
            for line in strings
            if line
        ])


@contextlib.contextmanager
def deep_recursion():
    old_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(100000)
        yield
    finally:
        sys.setrecursionlimit(old_limit)


HTML_REGISTRY = {
    'css': bake_parametrized(css_selector),
    'css-all': bake_parametrized(css_selector, select_all=True),
    'xpath': bake_parametrized(xpath_selector),
    'tag': bake_parametrized(tag_selector),
    'text': wrap_dummy(extract_text),
}
