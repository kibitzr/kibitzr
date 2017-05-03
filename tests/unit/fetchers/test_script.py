import pytest

from kibitzr.fetcher.script import fetch_by_script


def test_fetch_by_script_default_is_bash():
    ok, content = fetch_by_script(
        {'script': 'echo "hello"'}
    )
    assert ok is True
    assert content == "hello\n"


def test_fetch_by_explicit_bash_script():
    ok, content = fetch_by_script(
        {'script': {'bash': 'echo "hello"'}}
    )
    assert ok is True
    assert content == "hello\n"


def test_fetch_by_python_script():
    ok, content = fetch_by_script(
        {'script': {'python': 'ok, content = True, "hello"'}}
    )
    assert ok is True
    assert content == "hello"


def test_python_script_must_define_content():
    with pytest.raises(AssertionError):
        fetch_by_script(
            {'script': {'python': 'dummy'}}
        )


def test_python_script_exception_is_reported():
    ok, content = fetch_by_script(
        {'script': {'python': 'content = 1 / 0'}}
    )
    assert ok is False
    assert content.splitlines()[-1].startswith("ZeroDivisionError")


def test_ok_is_optional_in_python_script():
    ok, content = fetch_by_script(
        {'script': {'python': 'content = "dummy"'}}
    )
    assert ok is True
    assert content == "dummy"


def test_bash_error_is_returned():
    ok, content = fetch_by_script(
        {'script': 'no command not found'}
    )
    assert ok is False
    assert content.split(':', 1)[1].strip() == "line 1: no: command not found"
