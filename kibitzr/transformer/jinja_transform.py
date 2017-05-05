import logging
import json

import six
from jinja2 import Template, TemplateError
from bs4 import BeautifulSoup
from lxml import etree

from .utils import bake_parametrized
from .html import deep_recursion, extract_text


logger = logging.getLogger(__name__)


def jinja_transform(code, content, conf):
    html = LazyHTML(content)
    xml = LazyXML(content)
    context = {
        'conf': conf,
        'content': content,
        'lines': content.splitlines(),
        'json': LazyJSON(content),
        'css': html.css,
        'xpath': xml.xpath,
    }
    template = Template(code)
    template.environment.filters['text'] = text_filter
    try:
        return True, template.render(context)
    except TemplateError:
        logger.warning("Jinja transform failed", exc_info=True)
        return False, None


def text_filter(html):
    if isinstance(html, list):
        html = "".join(html)
    ok, content = extract_text(html)
    if ok:
        return content
    else:
        raise RuntimeError("Extract text failed")


class LazyJSON(object):
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


class LazyHTML(object):
    def __init__(self, content):
        self.html = content
        self._soup = None

    @property
    def soup(self):
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "html.parser")
        return self._soup

    def css(self, selector):
        with deep_recursion():
            elements = self.soup.select(selector)
            result = [six.text_type(x)
                      for x in elements]
            return result


class LazyXML(object):
    def __init__(self, content):
        self.xml = content
        self._root = None

    @property
    def root(self):
        if self._root is None:
            self._root = etree.fromstring(
                self.xml,
                parser=etree.HTMLParser(),
            )
        return self._root

    def xpath(self, selector):
        elements = self.root.xpath(selector)
        return [
            etree.tostring(
                element,
                method='html',
                pretty_print=True,
                encoding='unicode',
            )
            for element in elements
        ]


JINJA_REGISTRY = {
    'jinja': bake_parametrized(jinja_transform, pass_conf=True)
}
