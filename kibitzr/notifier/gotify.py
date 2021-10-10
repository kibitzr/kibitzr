import logging
import urllib3

from ..conf import settings


logger = logging.getLogger(__name__)


class GotifyNotify(object):
    def __init__(self, value):
        import requests
        self.session = requests.Session()
        gotify_creds = settings().creds['gotify']
        self.url = gotify_creds['url'].rstrip('/') + '/message'
        self.token = gotify_creds['token']
        self.verify = gotify_creds.get('verify', True)
        if not self.verify:
            # Since certificate validation was disabled, do not show the warning
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if value is None:
            value = {}
        self.title = value.get('title', 'kibitzr')
        self.priority = value.get('priority', 4)

    def post(self, report):
        logger.info("Executing Gotify notifier")
        response = self.session.post(
            url=self.url,
            json=self.json(report),
            params=self.params(),
            verify=self.verify
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
    __call__ = post

    def params(self):
        return {
            'token': self.token
        }

    def json(self, report):
        return {
            'title': self.title,
            'message': report,
            'priority': self.priority
        }


def notify_factory(conf, value):
    return GotifyNotify(value)
