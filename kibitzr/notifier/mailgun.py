from .webhook import WebHookNotify, webhook_factory

from ..conf import settings


class MailgunNotify(WebHookNotify):

    CREDS_KEY = 'mailgun'

    def __init__(self, conf, value, **kwargs):
        self.mailgun_creds = settings().creds.get('mailgun', {})
        self.mailgun_creds.update(value or {})
        domain = self.mailgun_creds['domain']
        self.context = {
            'subject': 'Kibitzr update for ' + conf['name'],
            'from': 'Kibitzr <mailgun@{0}>'.format(domain),
            'to': [self.mailgun_creds['to']],
        }
        super(MailgunNotify, self).__init__(conf=conf, value=value, **kwargs)

    def load_url(self, creds_key, value):
        return ('https://api.mailgun.net/v3/{0}/messages'
                .format(self.mailgun_creds['domain']))

    def configure_session(self):
        self.session.auth = ('api', self.mailgun_creds['key'])

    def payload(self, report):
        return dict(
            self.context,
            text=report,
        )


notify_factory = webhook_factory(MailgunNotify)
