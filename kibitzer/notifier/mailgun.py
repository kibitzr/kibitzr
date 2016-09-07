import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


def post_mailgun(conf, report, **kwargs):
    mailgun = settings().notifiers.get('mailgun', {})
    mailgun.update(settings().creds.get('mailgun', {}))
    subject = "Kibitzer update for " + conf['name']
    response = requests.post(
        "https://api.mailgun.net/v3/{domain}/messages"
        .format(domain=mailgun['domain']),
        auth=("api", mailgun['key']),
        data={
            "from": "Kibitzer <mailgun@{domain}>"
                    .format(domain=mailgun['domain']),
            "to": [mailgun['to']],
            "subject": subject,
            "text": report,
        })
    logger.debug(response.text)
    response.raise_for_status()
    return response
