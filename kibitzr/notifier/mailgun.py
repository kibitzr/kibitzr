import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


class MailgunNotify(object):

    def __init__(self, conf, value):
        mailgun_creds = settings().creds.get('mailgun', {})
        mailgun_creds.update(value or {})
        domain = mailgun_creds['domain']
        self.context = {
            'subject': 'Kibitzr update for ' + conf['name'],
            'from': 'Kibitzer <mailgun@{0}>'.format(domain),
            'to': [mailgun_creds['to']],
        }
        self.url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
        self.auth = ('api', mailgun_creds['key'])
        self.session = requests.Session()

    def __call__(self, report):
        response = self.session.post(
            self.url,
            auth=self.auth,
            data=self.payload(report),
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response

    def payload(self, report):
        return dict(
            self.context,
            text=report,
        )


def notify_factory(conf, value):
    return MailgunNotify(conf, value)
