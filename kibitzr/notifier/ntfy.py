import logging

from ..conf import settings


logger = logging.getLogger(__name__)


class NtfyNotify:
    def __init__(self, value):
        import requests  # pylint: disable=import-outside-toplevel
        self.session = requests.Session()
        ntfy_creds = settings().creds['ntfy']
        self.url = ntfy_creds.get('url')
        self.topic = ntfy_creds.get('topic')
        self.auth = ntfy_creds.get('auth', None)
        if self.auth:
            self.session.headers.update({'Authorization': self.auth})
        self.topic = ntfy_creds.get('topic')
        if value is None:
            value = {}
        if 'topic' in value:
            self.topic = value.get('topic')
        self.title = value.get('title', 'kibitzr')
        self.priority = str(value.get('priority', 3))

        self.url = f'{self.url.rstrip("/")}/{self.topic}'

    def post(self, report):
        logger.info("Executing ntfy notifier")
        response = self.session.post(
            url=self.url,
            headers=self.headers(),
            data=report,
        )
        logger.debug(response.text)
        response.raise_for_status()
    __call__ = post

    def headers(self):
        return {
            'X-Title': self.title,
            'X-Priority': self.priority
        }


def notify_factory(conf, value):
    return NtfyNotify(value)
