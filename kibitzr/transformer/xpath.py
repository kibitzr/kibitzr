import logging

import six

logger = logging.getLogger(__name__)


def parse_html(html):
    from defusedxml import lxml as dlxml
    from lxml import etree

    # lxml requires argument to be bytes
    # see https://github.com/kibitzr/kibitzr/issues/47
    encoded = html.encode('utf-8')
    return dlxml.fromstring(encoded, parser=etree.HTMLParser())


def xpath_selector(selector, html, select_all):
    """
    Returns Xpath match for `selector` within `html`.

    :param selector: XPath string
    :param html: Unicode content
    :param select_all: True to get all matches
    """
    from defusedxml import lxml as dlxml
    import re

    root = parse_html(html)
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
