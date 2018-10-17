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
    # Explicitly listing exceptions from above to make pylint happy:
    EXCEPTED = (
        requests.HTTPError,
        requests.ConnectionError,
        requests.Timeout,
    )

    def __init__(self, conf):
        self.conf = conf
        self.session = CacheControl(requests.Session())
        self.session.headers.update({
            'User-agent': 'Kibitzr/' + version,
        })
        self.url = conf['url']
        self.valid_http = set(conf.get('valid_http', [200]))
        self.verify_cert = conf.get('verify_cert', True)

    def fetch(self):
        retries = 3
        for retry in range(retries):
            try:
                response = self.session.get(self.url, timeout=(3.05, 27), verify=self.verify_cert)
            except self.EXCEPTED as exc:
                if retry < retries - 1:
                    self.sleep_on_exception(exc, retry)
                else:
                    raise
            else:
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


def requests_fetcher(conf):
    def fetcher():
        return session_fetcher.fetch()
    session_fetcher = SessionFetcher(conf)
    return fetcher
