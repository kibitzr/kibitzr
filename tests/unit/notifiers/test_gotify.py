import pytest
from kibitzr.notifier.gotify import GotifyNotify

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


def test_gotify_sample(settings):
    settings.creds.update({
        'gotify': {
            'url': 'http://localhost:8080',
            'token': '123456',
        }
    })
    value = {}
    notify = GotifyNotify(value=value)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url='http://localhost:8080/message',
        json={
            'title': 'kibitzr',
            'message': 'report',
            'priority': 4
        },
        params={'token': '123456'},
        verify=True
    )


def test_gotify_no_verification(settings):
    settings.creds.update({
        'gotify': {
            'url': 'https://localhost:8080',
            'token': '123456',
            'verify': False,
        }
    })
    value = {}
    notify = GotifyNotify(value=value)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url='https://localhost:8080/message',
        json={
            'title': 'kibitzr',
            'message': 'report',
            'priority': 4,
        },
        params={'token': '123456'},
        verify=False
    )


def test_gotify_override_defaults(settings):
    settings.creds.update({
        'gotify': {
            'url': 'http://localhost:8080',
            'token': '123456',
        }
    })
    value = {'title': 'Important Notification', 'priority': 7}
    notify = GotifyNotify(value=value)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url='http://localhost:8080/message',
        json={
            'title': 'Important Notification',
            'message': 'report',
            'priority': 7
        },
        params={'token': '123456'},
        verify=True
    )
