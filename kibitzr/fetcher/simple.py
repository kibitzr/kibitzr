import logging
import collections
from time import sleep

import requests
from kibitzr import __version__ as version


logger = logging.getLogger(__name__)


class SessionFetcher(object):
    RETRIABLE_EXCEPTIONS = (
        (requests.HTTPError, 5),
        (requests.ConnectionError, 15),
        (requests.Timeout, lambda retry: 60 * (retry + 1)),
    )
    EXCEPTED = tuple(exc for exc, _ in RETRIABLE_EXCEPTIONS)
    HEADERS_MAP = {
        'last-modified': 'If-Modified-Since',
        'etag': 'If-None-Match',
    }

    def __init__(self, conf):
        self.conf = conf
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent': 'Kibitzer/' + version,
        })
        self.url = conf['url']
        self.valid_http = set(conf.get('valid_http', [200, 304]))
        self.headers = dict.fromkeys(self.HEADERS_MAP.values(), None)
        self.cached_text = u''

    def fetch(self, *args, **_kwargs):
        retries = 3
        for retry in range(retries):
            try:
                response = self.session.get(self.url, headers=self.headers)
            except self.RETRIABLE_EXCEPTIONS as exc:
                if retry < retries - 1:
                    self.sleep_on_exception(exc, retry)
                else:
                    raise
            if response.status_code in (200, 304):
                self.update_cache(response)
            ok = (response.status_code in self.valid_http)
            return ok, response.text

    def sleep_on_exception(self, exc, retry):
        for klass, seconds in self.RETRIABLE_EXCEPTIONS:
            if isinstance(exc, klass):
                if isinstance(seconds, collections.Callable):
                    seconds = seconds(retry)
                sleep(seconds)
                break

    def update_cache(self, response):
        for response_key, request_key in self.HEADERS_MAP.items():
            value = response.headers.get(response_key)
            if value:
                self.headers[request_key] = value
                if response.text:
                    self.cached_text = response.text
        logger.debug("Headers: %r", self.headers)
        logger.debug("Cache Length: %d", len(self.cached_text))
