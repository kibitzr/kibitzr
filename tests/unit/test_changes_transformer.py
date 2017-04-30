import contextlib
import tempfile
import shutil
from kibitzr.storage import PageHistory


@contextlib.contextmanager
def history(style=None):
    storage_dir = tempfile.mkdtemp()
    page_history = PageHistory(
        conf={'name': 'test', 'url': 'web'},
        storage_dir=storage_dir,
        style=style,
    )
    try:
        yield page_history
    finally:
        shutil.rmtree(storage_dir)


def test_unified_diff_sample():
    with history('default') as page_history:
        scenario = (
            (u"hello", True, u"test at web\n@@ -0,0 +1 @@\n+hello"),
            (u"world", True, u"test at web\n@@ -1 +1 @@\n-hello\n+world"),
            (u"world", False, None),
        )
        for content, changed, report in scenario:
            result = page_history.report_changes(content)
            assert result == (changed, report)


def test_verbose_diff_sample():
    with history('verbose') as page_history:
        scenario = (
            (u"hello", True, u"test at web\nhello"),
            (u"world", True, u"test at web\n"
                             u"New value:\nworld\n"
                             u"Old value:\nhello\n"),
            (u"world", False, None),
        )
        for content, changed, report in scenario:
            result = page_history.report_changes(content)
            assert result == (changed, report)


def test_word_diff_sample():
    with history('word') as page_history:
        scenario = (
            (u"hello", True, u"hello"),
            (u"world", True, u"[-hello-]{+world+}"),
            (u"world", False, None),
        )
        for content, changed, report in scenario:
            r_changed, r_content = page_history.report_changes(content)
            assert r_changed == changed
            if r_content:
                assert r_content.splitlines()[0] == report
            else:
                assert r_content == report
