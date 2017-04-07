import contextlib

from kibitzr.conf import ReloadableSettings
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
            - slack
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
        'notify': ['slack'],
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
            settings = ReloadableSettings('')
    assert settings.pages == pages
    assert settings.creds == creds
    assert settings.notifiers == notifiers


@contextlib.contextmanager
def patch_source(method, data):
    fake_file = mock.mock_open(read_data=data)
    with mock.patch.object(ReloadableSettings,
                           method,
                           fake_file,
                           create=True) as fake_method:
        yield fake_method
