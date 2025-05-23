import pytest
from kibitzr.notifier.ntfy import NtfyNotify

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


def test_ntfy_default(settings):
    settings.creds.update({
        'ntfy': {
            'url': 'http://localhost:8080',
            'topic': 'secret-topic',
        }
    })
    value = {}
    notify = NtfyNotify(value=value)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url='http://localhost:8080/secret-topic',
        headers={'X-Title': 'kibitzr', 'X-Priority': '3'},
        data='report',
    )

    assert 'Authorization' not in notify.session.headers


def test_ntfy_override_defaults(settings):
    settings.creds.update({
        'ntfy': {
            'url': 'http://localhost:8080',
            'topic': 'secret-topic',
            'auth': 'Basic test',
        }
    })
    value = {'title': 'Important Notification', 'priority': 5, 'topic': 'another-topic'}
    notify = NtfyNotify(value=value)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url='http://localhost:8080/another-topic',
        headers={'X-Title': 'Important Notification', 'X-Priority': '5'},
        data='report',
    )

    assert 'Authorization' in notify.session.headers
    assert notify.session.headers['Authorization'] == 'Basic test'
