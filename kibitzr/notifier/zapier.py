import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


class ZapierSession(object):
    def __init__(self, url=None, *args, **kwargs):
        zapier_conf = settings().notifiers.get('zapier', {})
        zapier_conf.update(settings().creds.get('zapier', {}))
        if url is not None:
            zapier_conf.update({'url': url})
        self.url = zapier_conf['url']
        self.session = requests.Session()

    def post(self, report, **kwargs):
        response = self.session.post(
            url=self.url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"text": report},
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
