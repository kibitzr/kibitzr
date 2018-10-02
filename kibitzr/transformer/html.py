import sys
import contextlib
import logging
import functools

import six

from .utils import bake_parametrized


logger = logging.getLogger(__name__)


class SoupOps(object):
    def __init__(self, selector=None, select_all=False):
        self.selector = selector
        self.select_all = select_all

    def tag_selector(self, html):
        with soup(html) as doc:
            element = doc.find(self.selector)
            if element:
                return True, six.text_type(element)
            else:
                logger.warning('Tag not found: %r', self.selector)
                return False, html

    def css_selector(self, html):
        with soup(html) as doc:
            try:
                elements = doc.select(self.selector)
                if self.select_all:
                    result = u"".join(six.text_type(x)
                                      for x in elements)
                else:
                    result = six.text_type(elements[0])
                return True, result
            except IndexError:
                logger.warning('CSS selector not found: %r', self.selector)
                return False, html

    @staticmethod
    def extract_text(html):
        with soup(html) as doc:
            strings = doc.stripped_strings
            return True, u'\n'.join([
                line
                for line in strings
                if line
            ])

    @classmethod
    def factory(cls, key, value, conf):
        def transform(content):
            instance = cls(selector=value, select_all=select_all)
            method = handler.__get__(instance, cls)
            return method(content)
        action, _, all_flag = key.partition('-')
        select_all = (all_flag == 'all')
        handler = cls.SHORTCUTS[action]
        return transform

    SHORTCUTS = {
        'tag': tag_selector,
        'css': css_selector,
        'text': extract_text,
    }


def xpath_selector(selector, html, select_all):
    """
    Returns Xpath match for `selector` within `html`.

    :param selector: XPath string
    :param html: Unicode content
    :param select_all: True to get all matches
    """
    from defusedxml import lxml as dlxml
    from lxml import etree
    import re

    # lxml requires argument to be bytes
    # see https://github.com/kibitzr/kibitzr/issues/47
    encoded = html.encode('utf-8')
    root = dlxml.fromstring(encoded, parser=etree.HTMLParser())
    xpath_results = root.xpath(selector)
    if not xpath_results:
        logger.warning('XPath selector not found: %r', selector)
        return False, html

    if isinstance(xpath_results, list):
        if select_all is False:
            xpath_results = xpath_results[0:1]
    else:
        xpath_results = [xpath_results]

    # Serialize xpath_results
    # see https://lxml.de/xpathxslt.html#xpath-return-values
    results = []
    for r in xpath_results:
        # namespace declarations
        if isinstance(r, tuple):
            results.append("%s=\"%s\"" % (r[0], r[1]))
        # an element
        elif hasattr(r, 'tag'):
            results.append(
                re.sub(r'\s+', ' ',
                       dlxml.tostring(r, method='html', encoding='unicode'))
            )
        else:
            results.append(r)

    return True, u"\n".join(six.text_type(x).strip() for x in results)


@contextlib.contextmanager
def soup(html):
    from bs4 import BeautifulSoup
    with deep_recursion():
        yield BeautifulSoup(html, "html.parser")


@contextlib.contextmanager
def deep_recursion():
    old_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(100000)
        yield
    finally:
        sys.setrecursionlimit(old_limit)


def bake_html(key):
    return functools.partial(SoupOps.factory, key)


def register():
    """
    Return dictionary of tranform factories
    """
    registry = {
        key: bake_html(key)
        for key in ('css', 'css-all', 'tag', 'text')
    }
    registry['xpath'] = bake_parametrized(xpath_selector, select_all=False)
    registry['xpath-all'] = bake_parametrized(xpath_selector, select_all=True)
    return registry
