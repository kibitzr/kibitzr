from kibitzr.transformer.plain_text import (
    python_transform,
    bash_transform,
)


def test_bash_transform_sample():
    ok, content = bash_transform(
        code="sed 's/A/B/g'",
        content="ACTGA",
    )
    assert ok is True
    assert content == "BCTGB"


def test_python_transform_sample():
    ok, content = python_transform(
        code="content = content.replace('A', 'B')",
        content="ACTGA",
        conf=None,
    )
    assert ok is True
    assert content == "BCTGB"


def test_bash_transform_error_is_captured():
    ok, content = bash_transform(
        code="ls /NO-SUCH-DIR",
        content="?",
    )
    assert ok is False
    assert "ls: cannot access" in content
    assert "/NO-SUCH-DIR" in content
    assert "No such file or directory" in content


def test_python_exception_is_captured():
    ok, content = python_transform(
        code="content = 1 / 0",
        content="?",
        conf=None,
    )
    assert ok is False
    assert content.splitlines()[-1].startswith("ZeroDivisionError")


def test_empty_stdin_is_skipped():
    ok, content = bash_transform(
        code="no such command",
        content="",
    )
    assert ok is True
    assert "" == content
