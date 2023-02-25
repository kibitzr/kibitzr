import functools
import logging

import six
from twilio.rest import Client

from ..conf import settings

logger = logging.getLogger(__name__)


def notify_factory(conf, value):
    @functools.wraps(notify)
    def baked_notify(report):
        return notify(
            report=report,
            notifier_conf=value,
        )

    del conf
    return baked_notify


def notify(report, notifier_conf):
    logger.info("Executing Twilio notifier")
    credentials = settings().creds.get("twilio", {})
    account_sid = credentials.get("account_sid", "")
    auth_token = credentials.get("auth_token", "")
    src_phone_number = credentials.get("phone_number", "")
    try:
        recipients = notifier_conf["recipients"]
    except (TypeError, KeyError):
        recipients = notifier_conf
    if isinstance(recipients, six.string_types):
        recipients = [recipients]
    if not src_phone_number:
        src_phone_number = recipients[0]
    send_message(
        account_sid=account_sid,
        auth_token=auth_token,
        src_phone_number=src_phone_number,
        recipients=recipients,
        content=report,
    )


def send_message(account_sid, auth_token, src_phone_number, recipients, content):
    client = Client(account_sid, auth_token)
    for recipient in recipients:
        client.messages.create(
            body=content,
            from_=src_phone_number,
            to=recipient,
        )
