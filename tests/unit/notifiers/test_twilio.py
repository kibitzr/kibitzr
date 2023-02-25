import pytest
from twilio.rest import Client

from kibitzr.notifier.twilio import notify

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture(name='settings')
def settings_fixture():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


def test_twilio_sample(settings):
    settings.creds.update(
        {
            "twilio": {
                "account_sid": "sid",
                "auth_token": "token",
                "phone_number": "phone_number",
            }
        }
    )
    fake_client = mock.Mock(auto_spec=Client)
    notify(
        "report",
        notifier_conf={"recipients": ["recipient"]},
        client_factory=fake_client,
    )
    fake_client.assert_called_once_with("sid", "token")
    client_instance = fake_client.return_value
    client_instance.messages.create.assert_called_once_with(
        body="report",
        from_="phone_number",
        to="recipient",
    )
