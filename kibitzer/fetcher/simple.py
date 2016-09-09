import json

import requests

from kibitzer import __version__ as version


def simple_fetcher(conf):
    url = conf['url']
    output_format = conf.get('format', 'asis')
    response = requests.get(
        url=url,
        headers={'User-agent': 'Kibitzer/' + version},
    )
    ok = (response.status_code == 200)
    if ok and output_format == 'json':
        return ok, json.dumps(
            response.json(),
            indent=True,
            sort_keys=True,
            ensure_ascii=False,
            # encoding='utf-8',
        )
    else:
        return ok, response.text
