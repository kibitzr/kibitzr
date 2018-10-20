import pytest
from kibitzr.conf import (
    settings,
    ReloadableSettings,
    ConfigurationError,
)
from kibitzr.timeline import TimelineRule
from ..compat import mock
from .helpers import patch_conf, patch_creds


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

    - name: Alarm clock
      url: https://www.worldtimeserver.com/current_time_in_US-NY.aspx
      transform:
          - css: "span#theTime"
          - text
      notify:
          - python: print(content)
      schedule:
            every: day
            at: "6:30"

    - name: Noon alarm
      url: https://www.worldtimeserver.com/current_time_in_US-NY.aspx
      transform:
          - css: "span#theTime"
          - text
      notify:
          - python: print(content)
      schedule:
            every: 1
            unit: day
            at: "20:30"

    - name: Crazy scheduling alarm
      url: https://www.worldtimeserver.com/current_time_in_US-NY.aspx
      transform:
          - css: "span#theTime"
          - text
      notify:
          - python: print(content)
      schedule:
          - every: 1
            unit: days
            at: "15:30"
          - every: hour
          - every: 4
            unit: minutes
          - every: saturday
            at: "11:17"
"""

sample_creds = """
mailgun:
    url: ZZZ
"""


checks = [
    {
        'name': 'Project Build Status',
        'url': 'http://teamcity/build/id',
        'transforms': ['text', {'changes': 'verbose'}],
        'scenario': 'driver.find_element_by_css_selector(".login").click()\n',
        'notify': [{'smtp': 'kibitzrrr@gmail.com'}],
        'schedule': [TimelineRule(interval=60, unit='seconds', at=None)]
    },
    {
        'name': 'WordPress A Plugin',
        'url': "http://wordpress/A",
        'notify': ['mailgun'],
        'schedule': [TimelineRule(interval=300, unit='seconds', at=None)]
    },
    {
        'name': 'WordPress B Plugin',
        'url': "http://wordpress/B",
        'notify': ['mailgun'],
        'schedule': [TimelineRule(interval=300, unit='seconds', at=None)]
    },
    {
        'name': 'Alarm clock',
        'url': "https://www.worldtimeserver.com/current_time_in_US-NY.aspx",
        'transform': [{'css': 'span#theTime'}, 'text'],
        'notify': [{'python': 'print(content)'}],
        'schedule': [TimelineRule(interval=1, unit='day', at='6:30')]
    },
    {
        'name': 'Noon alarm',
        'url': "https://www.worldtimeserver.com/current_time_in_US-NY.aspx",
        'transform': [{'css': 'span#theTime'}, 'text'],
        'notify': [{'python': 'print(content)'}],
        'schedule': [TimelineRule(interval=1, unit='day', at='20:30')]
    },
    {
        'name': 'Crazy scheduling alarm',
        'url': "https://www.worldtimeserver.com/current_time_in_US-NY.aspx",
        'transform': [{'css': 'span#theTime'}, 'text'],
        'notify': [{'python': 'print(content)'}],
        'schedule': [
            TimelineRule(interval=1, unit='days', at='15:30'),
            TimelineRule(interval=1, unit='hour', at=None),
            TimelineRule(interval=4, unit='minutes', at=None),
            TimelineRule(interval=1, unit='saturday', at='11:17')
        ]
    },
]

creds = {
    'mailgun': {'url': 'ZZZ'},
}

notifiers = {
    'slack': {'url': 'XXX'},
}


def test_complex_conf_sample():
    with patch_conf(sample_conf):
        with patch_creds(sample_creds):
            conf = ReloadableSettings('::')
    assert conf.checks == checks
    assert conf.creds['mailgun']['url'] == 'ZZZ'


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
    with patch_creds(""):
        with patch_conf(conf1):
            conf = ReloadableSettings('::')
            # Config didn't change:
            assert not conf.reread()
        with patch_conf(conf2):
            # Config changed:
            assert conf.reread()
    assert conf.checks == [{
        'name': 'Name',
        'url': 'URL',
        'schedule': [TimelineRule(interval=60, unit='seconds', at=None)]
    }]


def test_name_from_url_population():
    conf = "checks: [{url: 'http://example.com/page_name'}]"
    with patch_conf(conf):
        conf = ReloadableSettings('::')
    assert conf.checks[0]['name'] == 'http-example-com-page_name'


def test_unnamed_check():
    conf = "checks: [{period: 1}]"
    with patch_conf(conf):
        conf = ReloadableSettings('::')
    assert conf.checks == [{
        'name': 'Unnamed check 1',
        'schedule': [TimelineRule(interval=1, unit='seconds', at=None)]
    }]
