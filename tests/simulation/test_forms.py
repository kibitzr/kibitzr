import time
from kibitzr.checker import Checker


def test_fill_form_sample(target):
    conf = {
        'name': 'Test page',
        'url': "http://{0}:{1}/form.html".format(*target),
        'form': [
            {'id': 'name', 'value': '{{ "name" | sort | join("") }}'},
            {'css': '#pass', 'creds': 'pass'}
        ],
        # 'scenario': 'import pdb; pdb.set_trace()',
        'transform': [{'css': '.unclosed-tag > #params'}, 'text'],
        # 'headless': False,
    }
    total_attempts = 3
    for attempt in range(total_attempts):
        try:
            ok, content = Checker(conf).check()
        except TypeError:
            if attempt == total_attempts - 1:
                raise
            # Maybe HTTP server haven't started yet?..
            time.sleep(1.0)
            continue
        else:
            break
    assert ok is True
    assert content == "\n".join([
        "name = aemn",
        "pass = password",
    ])
