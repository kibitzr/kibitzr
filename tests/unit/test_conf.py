import contextlib

import pytest
from kibitzr.conf import settings, ReloadableSettings, ConfigurationError
from ..compat import mock


sample_conf = """
notifiers:
    slack:
        url: XXX

templates:
    teamcity:
        transforms:
            - text
            - changes: verbose
        scenario:
            login
        notify:
            - smtp: kibitzrrr@gmail.com
        period: 3600

scenarios:
    login: |
        driver.find_element_by_css_selector(".login").click()

checks:
    - name: Project Build Status
      url: http://teamcity/build/id
      template: teamcity
      period: 60

    - batch: WordPress {0} Plugin
      url-pattern: "http://wordpress/{0}"
      notify:
        - mailgun
      items:
        - A
        - B
"""

sample_creds = """
mailgun:
    url: ZZZ
"""


pages = [
    {
        'name': 'Project Build Status',
        'url': 'http://teamcity/build/id',
        'transforms': ['text', {'changes': 'verbose'}],
        'scenario': 'driver.find_element_by_css_selector(".login").click()\n',
        'notify': [{'smtp': 'kibitzrrr@gmail.com'}],
        'period': 60,
    },
    {
        'name': 'WordPress A Plugin',
        'url': "http://wordpress/A",
        'notify': ['mailgun'],
    },
    {
        'name': 'WordPress B Plugin',
        'url': "http://wordpress/B",
        'notify': ['mailgun'],
    },
]

creds = {
    'mailgun': {'url': 'ZZZ'},
}

notifiers = {
    'slack': {'url': 'XXX'},
}


def test_complex_conf_sample():
    with patch_source("open_conf", sample_conf):
        with patch_source("open_creds", sample_creds):
            conf = ReloadableSettings('::')
    assert conf.pages == pages
    assert conf.creds == creds
    assert conf.notifiers == notifiers


@contextlib.contextmanager
def patch_source(method, data):
    fake_file = mock.mock_open(read_data=data)
    with mock.patch.object(ReloadableSettings,
                           method,
                           fake_file,
                           create=True) as fake_method:
        yield fake_method


@mock.patch("kibitzr.conf.os.path.exists", return_value=False)
def test_missing_config_raises_configuration_error(exists):
    with pytest.raises(ConfigurationError):
        settings()


def test_reread():
    conf1 = (
        "checks:\n"
        "  - name: Name\n"
        "    url: URL\n"
    )
    conf2 = conf1 + "    period: 60\n"
    with patch_source("open_creds", ""):
        with patch_source("open_conf", conf1):
            conf = ReloadableSettings('::')
            # Config didn't change:
            assert not conf.reread()
        with patch_source("open_conf", conf2):
            # Config changed:
            assert conf.reread()
    assert conf.pages == [{'name': 'Name', 'url': 'URL', 'period': 60}]


def test_name_from_url_population():
    conf = "checks: [{url: 'http://example.com/page_name'}]"
    with patch_source("open_conf", conf):
        conf = ReloadableSettings('::')
    assert conf.pages == [{
        'name': 'http-example-com-page_name',
        'url': 'http://example.com/page_name',
    }]


def test_unnamed_check():
    conf = "checks: [{period: 1}]"
    with patch_source("open_conf", conf):
        conf = ReloadableSettings('::')
    assert conf.pages == [{
        'name': 'Unnamed check 1',
        'period': 1,
    }]
