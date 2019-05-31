import pytest
from kibitzr.transformer.jinja_transform import JinjaTransform

from ...helpers import stash_mock


def jinja_transform(code, content, conf=None):
    return JinjaTransform(code, conf or {})(content)


def test_content_is_passed():
    ok, content = jinja_transform('hello {{ content }}!', 'world')
    assert ok is True
    assert content == "hello world!"


def test_lines_are_passed():
    ok, content = jinja_transform('{{ lines[1] }}', 'a\nb')
    assert ok is True
    assert content == "b"


def test_json_is_passed():
    ok, content = jinja_transform('{{ json["a"][1] }}', '{"a": [1, 2, 3]}')
    assert ok is True
    assert content == "2"


def test_css_selector_is_passed():
    ok, content = jinja_transform(
        '{{ css("div p") | text }}',
        '<div><a>A</a><p>P</p></div>',
    )
    assert ok is True
    assert content == "P"


# For possible types of xpath evaluation:
# https://lxml.de/xpathxslt.html#xpath-return-values
@pytest.mark.parametrize("selector,expected", [
    pytest.param("//div/p", "P", id="elements"),
    pytest.param("//a/@href", "#", id="attributes"),
    pytest.param("string(//p)", "P", id="string"),
    pytest.param("count(//p)", "1.0", id="float"),
    pytest.param("true()", "True", id="boolean"),
    ])
def test_xpath_selector_is_passed(selector, expected):
    code = '{{ xpath("%s") | text }}' % selector

    ok, content = jinja_transform(
        code,
        '<div><a href="#">A</a><p>P</p></div>'
        )
    assert ok is True
    assert content == expected


def test_stash_is_passed():
    with stash_mock() as stash:
        stash.write({'key': 'good'})
        ok, content = jinja_transform('{{ stash.key }} news', '')
        assert ok is True
        assert content == 'good news'
