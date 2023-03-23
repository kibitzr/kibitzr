import functools
import logging

import six

from ..conf import settings

logger = logging.getLogger(__name__)


def notify_factory(conf, value):
    @functools.wraps(notify)
    def baked_notify(report):
        from twilio.rest import Client  # pylint: disable=import-outside-toplevel
        return notify(
            report=report,
            notifier_conf=value,
            client_factory=Client,
        )

    del conf
    return baked_notify


def notify(report, notifier_conf, client_factory):
    logger.info("Executing Twilio notifier")
    credentials = settings().creds.get("twilio", {})
    account_sid = credentials.get("account_sid", "")
    auth_token = credentials.get("auth_token", "")
    src_phone_number = credentials.get("phone_number", "")
    client = client_factory(account_sid, auth_token)
    try:
        recipients = notifier_conf["recipients"]
    except (TypeError, KeyError):
        recipients = notifier_conf
    if isinstance(recipients, six.string_types):
        recipients = [recipients]
    if not src_phone_number:
        src_phone_number = recipients[0]
    for recipient in recipients:
        client.messages.create(
            body=report,
            from_=src_phone_number,
            to=recipient,
        )
