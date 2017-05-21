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
    ok, content = run_transform('xpath', '//body/h2/a[@id="page-link"]', HTML)
    assert ok is True
    assert content.strip() == '<a href="page.html" id="page-link">Page</a>'


def test_extract_test():
    ok, content = run_transform('text', None, HTML)
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
