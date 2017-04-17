import pytest
from kibitzr.notifier import smtp

from ..compat import mock
from ..helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


@mock.patch.object(smtp, 'send_email')
def test_smtp_shortcut(fake_send_email, settings):
    settings.creds.update({
        'smtp': {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
        }
    })
    smtp.post_smtp({'name': 'Name'}, 'report', 'you@site.com')
    fake_send_email.assert_called_once_with(
        user='user',
        password='password',
        recipients=['you@site.com'],
        subject='Kibitzr update for Name',
        body='report',
        host='host',
        port='port',
    )


@mock.patch.object(smtp, 'send_email')
def test_smtp_explicit_form(fake_send_email, settings):
    settings.creds.update({
        'smtp': {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
        }
    })
    smtp.post_smtp(
        {'name': 'Name'},
        'report',
        {'recipients': ['you@site.com'], 'subject': 'subject'},
    )
    fake_send_email.assert_called_once_with(
        user='user',
        password='password',
        recipients=['you@site.com'],
        subject='subject',
        body='report',
        host='host',
        port='port',
    )
