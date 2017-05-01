from kibitzr.transformer.jinja_transform import jinja_transform


def test_content_is_passed():
    ok, content = jinja_transform('world', 'hello {{ content }}!', {})
    assert ok is True
    assert content == "hello world!"


def test_lines_are_passed():
    ok, content = jinja_transform('a\nb', '{{ lines[1] }}', {})
    assert ok is True
    assert content == "b"


def test_json_is_passed():
    ok, content = jinja_transform('{"a": [1, 2, 3]}', '{{ json["a"][1] }}', {})
    assert ok is True
    assert content == "2"


def test_css_selector_is_passed():
    ok, content = jinja_transform(
        '<div><a>A</a><p>P</p></div>',
        '{{ css("div p") | text }}',
        {},
    )
    assert ok is True
    assert content == "P"


def test_xpath_selector_is_passed():
    ok, content = jinja_transform(
        '<div><a>A</a><p>P</p></div>',
        '{{ xpath("//div/p") | text }}',
        {},
    )
    assert ok is True
    assert content == "P"
