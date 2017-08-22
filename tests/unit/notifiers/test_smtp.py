import pytest
from kibitzr.notifier import smtp
from kibitzr.notifier import notify_factory

from ...compat import mock
from ...helpers import SettingsMock


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
    smtp.notify({'name': 'Name'}, 'report', 'you@site.com')
    fake_send_email.assert_called_once_with(
        user='user',
        password='password',
        recipients=['you@site.com'],
        subject='Kibitzr update for Name',
        body='report',
        host='host',
        port='port',
    )


@mock.patch('kibitzr.notifier.smtp.SMTP')
def test_smtp_explicit_form(fake_smtp, settings):
    settings.creds.update({
        'smtp': {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
        }
    })
    smtp.notify(
        {'name': 'Name'},
        'report',
        {'recipients': ['you@site.com'], 'subject': 'subject'},
    )
    fake_smtp.assert_called_once_with('host', 'port')
    fake_smtp.return_value.login.assert_called_once_with('user', 'password')
    fake_smtp.return_value.sendmail.assert_called_once_with(
        'user',
        ['you@site.com'],
        b'From: user\r\nTo: you@site.com\r\nSubject: subject\r\n\r\nreport\r\n',
    )


@mock.patch.object(smtp, 'send_email')
def test_config_is_passed(fake_send_email, settings):
    settings.creds.update({
        'smtp': {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
        }
    })
    notifier = notify_factory({
        'name': 'subject',
        'notify': [{'smtp': 'you@site.com'}]
    })
    notifier.notify(
        'report',
    )
    fake_send_email.assert_called_once_with(
        user='user',
        password='password',
        recipients=['you@site.com'],
        subject='Kibitzr update for subject',
        body='report',
        host='host',
        port='port',
    )


@mock.patch('kibitzr.notifier.smtp.SMTP')
def test_smtp_uses_local_server_by_default(fake_smtp, settings):
    settings.creds.pop('smtp', None)
    smtp.notify(
        {'name': 'Name'},
        'report',
        'you@site.com',
    )
    fake_smtp.assert_called_once_with('localhost', 25)
    fake_smtp.return_value.login.assert_called_once_with('you@site.com', '')
    fake_smtp.return_value.sendmail.assert_called_once_with(
        'you@site.com',
        ['you@site.com'],
        b'From: you@site.com\r\nTo: you@site.com\r\n'
        b'Subject: Kibitzr update for Name\r\n\r\nreport\r\n',
    )
