from .webhook import WebHookNotify, webhook_factory

from ..conf import settings


class MailgunNotify(WebHookNotify):

    CREDS_KEY = 'mailgun'

    def __init__(self, conf, value, **kwargs):
        self.mailgun_creds = settings().creds.get('mailgun', {})
        self.mailgun_creds.update(value or {})
        domain = self.mailgun_creds['domain']
        self.context = {
            'subject': f"Kibitzr update for {conf['name']}",
            'from': f'Kibitzr <mailgun@{domain}>',
            'to': [self.mailgun_creds['to']],
        }
        super().__init__(conf=conf, value=value, **kwargs)

    def load_url(self, creds_key, value):
        return f"https://api.mailgun.net/v3/{self.mailgun_creds['domain']}/messages"

    def configure_session(self):
        self.session.auth = ('api', self.mailgun_creds['key'])

    def payload(self, report):
        return dict(
            self.context,
            text=report,
        )


notify_factory = webhook_factory(MailgunNotify)
