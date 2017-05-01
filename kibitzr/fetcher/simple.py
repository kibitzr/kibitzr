import logging
import collections
from time import sleep

import requests
from cachecontrol import CacheControl
from kibitzr import __version__ as version


logger = logging.getLogger(__name__)


class SessionFetcher(object):
    RETRIABLE_EXCEPTIONS = (
        (requests.HTTPError, 5),
        (requests.ConnectionError, 15),
        (requests.Timeout, lambda retry: 60 * (retry + 1)),
    )
    EXCEPTED = tuple(exc for exc, _ in RETRIABLE_EXCEPTIONS)

    def __init__(self, conf):
        self.conf = conf
        self.session = CacheControl(requests.Session())
        self.session.headers.update({
            'User-agent': 'Kibitzer/' + version,
        })
        self.url = conf['url']
        self.valid_http = set(conf.get('valid_http', [200, 304]))

    def fetch(self, *args, **_kwargs):
        retries = 3
        for retry in range(retries):
            try:
                response = self.session.get(self.url)
            except self.RETRIABLE_EXCEPTIONS as exc:
                if retry < retries - 1:
                    self.sleep_on_exception(exc, retry)
                else:
                    raise
            ok = (response.status_code in self.valid_http)
            text = response.text
            return ok, text

    def sleep_on_exception(self, exc, retry):
        for klass, seconds in self.RETRIABLE_EXCEPTIONS:
            if isinstance(exc, klass):
                if isinstance(seconds, collections.Callable):
                    seconds = seconds(retry)
                sleep(seconds)
                break
