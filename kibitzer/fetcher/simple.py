import json

import requests


def simple_fetcher(conf):
    url = conf['url']
    output_format = conf.get('format', 'asis')
    response = requests.get(url)
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
