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
        self.priority = value.get('priority', 3)

    def post(self, report):
        logger.info("Executing ntfy notifier")
        response = self.session.post(
            url=self.url,
            json=self.json(report),
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
    __call__ = post

    def json(self, report):
        return {
            'topic': self.topic,
            'title': self.title,
            'message': report,
            'priority': self.priority
        }


def notify_factory(conf, value):
    return NtfyNotify(value)
