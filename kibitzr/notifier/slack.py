import json
import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


class SlackSession(object):
    def __init__(self, *args, **kwargs):
        slack = settings().notifiers.get('slack', {})
        slack.update(settings().creds.get('slack', {}))
        self.session = requests.Session()
        self.url = slack['url']

    def post(self, report, **kwargs):
        response = self.session.post(
            url=self.url,
            data={"payload": json.dumps({"text": report})},
        )
        logger.debug(response.text)
        response.raise_for_status()
        return response
