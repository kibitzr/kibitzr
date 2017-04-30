from bs4 import BeautifulSoup

from kibitzr.transformer.html import (
    tag_selector,
    css_selector,
    xpath_selector,
    extract_text,
)


def test_tag_selector():
    ok, content = tag_selector('a', HTML)
    assert ok is True
    assert content == '<a href="page.html" id="page-link">Page</a>'


def test_css_selector():
    ok, content = css_selector('body h2.nav a#page-link', HTML)
    assert ok is True
    assert content == '<a href="page.html" id="page-link">Page</a>'


def test_css_selector_all():
    ok, content = css_selector('div', HTML, select_all=True)
    assert ok is True
    assert prettify(content) == '\n'.join([
        '<div id="content">',
        ' Hello world!',
        '</div>',
        '',
        '<div class="footer">',
        ' Footer content',
        '</div>',
    ])


def test_xpath_selector():
    ok, content = xpath_selector('//body/h2/a[@id="page-link"]', HTML)
    assert ok is True
    assert content.strip() == '<a href="page.html" id="page-link">Page</a>'


def test_extract_test():
    ok, content = extract_text(HTML)
    assert ok is True
    assert content.strip() == "\n".join([
        "Page",
        "Hello world!",
        "Footer content",
    ])


HTML = """
<html>
    <body>
        <h2 class="header nav">
            <a href="page.html" id="page-link">Page</a>
        </h2>
        <div id="content">
            Hello world!
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
