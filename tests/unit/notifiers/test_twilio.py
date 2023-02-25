import pytest
from kibitzr.notifier.twilio import notify

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


@mock.patch('kibitzr.notifier.twilio.Client', spec=True)
def test_twilio_sample(fake_client, settings):  # pylint: disable=redefined-outer-name
    settings.creds.update({
        'twilio': {
            'account_sid': 'sid',
            'auth_token': 'token',
            'phone_number': 'phone_number',
        }
    })
    notify('report', notifier_conf={'recipients': ['recipient']})
    fake_client.assert_called_once_with('sid', 'token')
    client_instance = fake_client.return_value
    client_instance.messages.create.assert_called_once_with(
        body='report',
        from_='phone_number',
        to='recipient',
    )
