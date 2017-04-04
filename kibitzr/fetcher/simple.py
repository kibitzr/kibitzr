from time import sleep
import requests

from kibitzr import __version__ as version


class SessionFetcher(object):
    def __init__(self, conf):
        self.conf = conf
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent': 'Kibitzer/' + version,
        })
        self.url = conf['url']
        self.valid_http = set(conf.get('valid_http', [200]))

    def fetch(self, *args, **_kwargs):
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
            ok = (response.status_code in self.valid_http)
            return ok, response.text
