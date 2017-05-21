import logging

from ..conf import settings


logger = logging.getLogger(__name__)


class WebHookNotify(object):

    CREDS_KEY = 'webhook'
    POST_KEY = 'message'

    def __init__(self, creds_key=None, conf=None, value=None, post_key=None):
        import requests
        self.session = requests.Session()
        self.url = self.load_url(creds_key or self.CREDS_KEY, value)
        self.post_key = post_key or self.POST_KEY
        self.configure_session()

    def load_url(self, creds_key, value):
        if value:
            return value
        else:
            webhook_creds = settings().creds[creds_key]
            return webhook_creds['url']

    def post(self, report):
        response = self.session.post(
            self.url,
            data=self.payload(report),
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
    __call__ = post

    def configure_session(self):
        pass

    def payload(self, report):
        return {self.post_key: report}


def webhook_factory(klass):
    def notify_factory(conf, value):
        return klass(conf=conf, value=value)
    return notify_factory
