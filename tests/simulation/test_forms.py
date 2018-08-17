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
    ok, content = Checker(conf).check()
    assert ok is True
    assert content == "\n".join([
        "name = aemn",
        "pass = password",
    ])
