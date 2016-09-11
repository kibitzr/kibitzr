import requests

from kibitzer import __version__ as version


def simple_fetcher(conf):
    response = requests.get(
        url=conf['url'],
        headers={'User-agent': 'Kibitzer/' + version},
    )
    ok = (response.status_code == 200)
    return ok, response.text
