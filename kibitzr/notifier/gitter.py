import logging

import requests

from ..conf import settings


logger = logging.getLogger(__name__)


def post_gitter(conf, report, **kwargs):
    gitter = settings().notifiers.get('gitter', {})
    gitter.update(settings().creds.get('gitter', {}))
    response = requests.post(
        gitter['url'],
        data={"message": report},
    )
    logger.debug(response.text)
    response.raise_for_status()
    return response
