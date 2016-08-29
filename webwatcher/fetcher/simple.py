import json

import requests


def simple(conf):
    url = conf['url']
    output_format = conf.get('format', 'html')
    response = requests.get(url)
    if output_format == 'json':
        return json.dumps(response.json(), indent=True, sort_keys=True)
    else:
        return response.text
