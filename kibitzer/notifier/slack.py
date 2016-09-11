import json
import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


def post_slack(conf, report, **kwargs):
    slack = settings().notifiers.get('slack', {})
    slack.update(settings().creds.get('slack', {}))
    response = requests.post(
        url=slack['url'],
        data={"payload": json.dumps({"text": report})},
    )
    logger.debug(response.text)
    response.raise_for_status()
    return response
