from time import sleep
import requests

from kibitzr import __version__ as version


def simple_fetcher(conf):
    retries = 3
    for retry in range(retries):
        try:
            response = requests.get(
                url=conf['url'],
                headers={'User-agent': 'Kibitzer/' + version},
            )
        except requests.HTTPError:
            if retry == retries - 1:
                raise
            else:
                sleep(5)
                continue
        ok = (response.status_code == 200)
        return ok, response.text


class SessionFetcher(object):
    def __init__(self, conf):
        self.conf = conf
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent': 'Kibitzer/' + version,
        })
        self.url = conf['url']

    def fetch(self, *args, **kwargs):
        retries = 3
        for retry in range(retries):
            try:
                response = self.session.get(self.url)
            except requests.HTTPError:
                if retry == retries - 1:
                    raise
                else:
                    sleep(5)
                    continue
            ok = (response.status_code == 200)
            return ok, response.text
