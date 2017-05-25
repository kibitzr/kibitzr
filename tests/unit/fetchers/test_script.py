import pytest

from kibitzr.fetcher.script import fetch_by_script

from ...helpers import stash_mock


def run_script(script):
    return fetch_by_script({'script': script})


def test_fetch_by_script_default_is_bash():
    ok, content = run_script('echo hello')
    assert ok is True
    assert content.strip() == "hello"


def test_fetch_by_explicit_bash_script():
    ok, content = run_script({'bash': 'echo "hello"'})
    assert ok is True
    assert content == "hello\n"


def test_fetch_by_python_script():
    ok, content = run_script({'python': 'ok, content = True, "hello"'})
    assert ok is True
    assert content == "hello"


def test_python_script_must_define_content():
    with pytest.raises(AssertionError):
        run_script({'python': 'dummy'})


def test_python_script_exception_is_reported():
    ok, content = run_script({'python': 'content = 1 / 0'})
    assert ok is False
    assert content.splitlines()[-1].startswith("ZeroDivisionError")


def test_ok_is_optional_in_python_script():
    ok, content = run_script({'python': 'content = "dummy"'})
    assert ok is True
    assert content == "dummy"


def test_bash_error_is_returned():
    ok, content = run_script('no command not found')
    assert ok is False
    assert content.split(':', 1)[1].strip() == "line 1: no: command not found"


def test_python_script_has_stash():
    with stash_mock() as stash:
        stash.write({'key': 'value'})
        ok, content = run_script({'python': 'content = stash["key"]'})
        assert ok is True
        assert content == "value"
