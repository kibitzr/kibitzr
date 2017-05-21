import pytest
from kibitzr.notifier import notify_factory

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


def test_mailgun_sample(settings):
    settings.creds.update({
        'mailgun': {
            'key': 'key',
            'domain': 'domain',
            'to': 'to',
        }
    })
    notify = notify_factory({
        'name': 'subject',
        'notify': [{'mailgun': {'to': 'me'}}]
    })
    with mock.patch.object(notify.notifiers[0], "session") as fake_session:
        notify('report')
        fake_session.post.assert_called_once_with(
            'https://api.mailgun.net/v3/domain/messages',
            data={
                'to': ['me'],
                'text': 'report',
                'from': 'Kibitzr <mailgun@domain>',
                'subject': 'Kibitzr update for subject',
            }
        )
