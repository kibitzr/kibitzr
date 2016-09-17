import requests
from kibitzr.checker import Checker


def test_server_is_alive(target):
    """Sanity check, that test environment is properly setup"""
    response = requests.get("http://{0}:{1}/index.html".format(*target))
    assert response.status_code == 200


def test_simple_fetcher_with_pretty_json(target, json_conf):
    ok, content = Checker(json_conf).check()
    assert ok is True
    assert content == (
        '{\n'
        '  "first name": "Peter",\n'
        '  "last name": "Demin"\n'
        '}'
    )


def test_tag_transformer(target, html_text_conf):
    html_text_conf['transform'].insert(0, {
        'tag': 'div',
    })
    ok, content = Checker(html_text_conf).check()
    assert ok is True
    assert content == 'Hello world!'


def test_browser_css(target, html_text_conf):
    html_text_conf['transform'].insert(0, {
        'css': '.footer',
    })
    ok, content = Checker(html_text_conf).check()
    assert ok is True
    assert content == 'Footer content'


def test_browser_xpath(target, html_text_conf):
    html_text_conf['transform'].insert(0, {
        'xpath': './/*[@class="footer"]',
    })
    ok, content = Checker(html_text_conf).check()
    assert ok is True
    assert content == 'Footer content'


def test_scenario(target, html_text_conf):
    html_text_conf.update({
        'scenario': 'driver.find_element_by_id("page-link").click()'
    })
    ok, content = Checker(html_text_conf).check()
    assert ok is True
    assert content == 'Another page'
