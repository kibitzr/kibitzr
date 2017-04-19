import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


class ZapierSession(object):
    def __init__(self, *args, **kwargs):
        zapier_conf = settings().notifiers.get('zapier', {})
        zapier_conf.update(settings().creds.get('zapier', {}))
        self.url = zapier_conf['url']
        self.session = requests.Session()

    def post(self, report, **kwargs):
        response = self.session.post(
            url=self.url,
            data={"text": report},
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
