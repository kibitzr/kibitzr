import pytest
from kibitzr.notifier import notify_factory

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


@mock.patch("kibitzr.notifier.webhook.requests.Session")
def test_mailgun_sample(fake_session, settings):
    settings.creds.update({
        'mailgun': {
            'key': 'key',
            'domain': 'domain',
            'to': 'to',
        }
    })
    notify_func = notify_factory({
        'name': 'subject',
        'notify': [{'mailgun': {'to': 'me'}}]
    })
    notify_func('report')
    fake_session.return_value.post.assert_called_once_with(
        'https://api.mailgun.net/v3/domain/messages',
        data={
            'to': ['me'],
            'text': 'report',
            'from': 'Kibitzr <mailgun@domain>',
            'subject': 'Kibitzr update for subject',
        }
    )
