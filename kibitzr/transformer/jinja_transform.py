import re
import os
import logging
import json
import functools

import six

from kibitzr.stash import LazyStash
from .html import deep_recursion, SoupOps
from .xpath import parse_html, serialize_xpath_results

logger = logging.getLogger(__name__)


class JinjaTransform:

    def __init__(self, code, conf):
        from jinja2 import Environment  # pylint: disable=import-outside-toplevel
        environment = Environment()
        environment.filters['text'] = text_filter
        environment.filters['int'] = int_filter
        environment.filters['float'] = float_filter
        environment.filters['dollars'] = dollars_filter
        self.template = environment.from_string(code)
        self.conf = conf

    def render(self, content, context=None):
        from jinja2 import TemplateError  # pylint: disable=import-outside-toplevel
        try:
            return True, self.template.render(context or self.context(content))
        except TemplateError:
            logger.warning("Jinja render failed", exc_info=True)
            return False, None
    __call__ = render

    def context(self, content):
        html = LazyHTML(content)
        xml = LazyXML(content)
        return {
            'conf': self.conf,
            'stash': LazyStash(),
            'content': content,
            'lines': content.splitlines(),
            'json': LazyJSON(content),
            'css': html.css,
            'xpath': xml.xpath,
            'env': os.environ,
        }


RE_NOT_FLOAT = re.compile(r'[^0-9\.]')


def ignore_cast_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            logger.warning("Invalid value passed in Jinja transform",
                           exc_info=True)
            return None
    return wrapper


@ignore_cast_error
def dollars_filter(number):
    sign = '-' if number < 0 else ''
    return f"{sign}${abs(number):,}"


@ignore_cast_error
def int_filter(text):
    return int(text)


@ignore_cast_error
def float_filter(text):
    return float(RE_NOT_FLOAT.sub('', text))


def text_filter(html):
    if isinstance(html, list):
        html = "".join(html)
    ok, content = SoupOps.extract_text(html)
    if ok:
        return content
    else:
        raise RuntimeError("Extract text failed")


class LazyJSON:
    def __init__(self, content):
        self.text = content
        self._json = None

    @property
    def json(self):
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

    def __getitem__(self, key):
        return self.json[key]


class LazyHTML:
    def __init__(self, content):
        self.html = content
        self._soup = None

    @property
    def soup(self):
        from bs4 import BeautifulSoup  # pylint: disable=import-outside-toplevel
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "html.parser")
        return self._soup

    def css(self, selector):
        with deep_recursion():
            elements = self.soup.select(selector)
            result = [six.text_type(x)
                      for x in elements]
            return result


class LazyXML:
    def __init__(self, content):
        self.xml = content
        self._root = None

    @property
    def root(self):
        if self._root is None:
            self._root = parse_html(self.xml)
        return self._root

    def xpath(self, selector):
        elements = self.root.xpath(selector)
        return serialize_xpath_results(elements, select_all=True)


def register():
    return {
        'jinja': JinjaTransform,
    }
