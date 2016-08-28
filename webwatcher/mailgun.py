import logging

import requests

from .settings import NOTIFIERS


logger = logging.getLogger(__name__)


def post_mailgun(conf, report):
    mailgun = NOTIFIERS['mailgun']
    subject = "WebWatcher notification for " + conf['name']
    response = requests.post(
        "https://api.mailgun.net/v3/{domain}/messages"
        .format(domain=mailgun['domain']),
        auth=("api", mailgun['key']),
        data={
            "from": "Web Watcher <mailgun@{domain}>"
                    .format(domain=mailgun['domain']),
            "to": [mailgun['to']],
            "subject": subject,
            "text": report,
        })
    logger.debug(response.text)
    response.raise_for_status()
    return response
