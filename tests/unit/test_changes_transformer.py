import functools
import tempfile
import shutil
from kibitzr.storage import PageHistory


def history(style=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner():
            storage_dir = tempfile.mkdtemp()
            page_history = PageHistory(
                conf={'name': 'test', 'url': 'web'},
                storage_dir=storage_dir,
                style=style,
            )
            try:
                func(page_history)
            finally:
                shutil.rmtree(storage_dir)
        return inner
    return wrapper


@history('default')
def test_unified_diff_sample(page_history):
    scenario = (
        (u"hello", True, u"test at web\n@@ -0,0 +1 @@\n+hello"),
        (u"world", True, u"test at web\n@@ -1 +1 @@\n-hello\n+world"),
        (u"world", False, None),
    )
    for content, changed, report in scenario:
        result = page_history.report_changes(content)
        assert result == (changed, report)


@history('verbose')
def test_verbose_diff_sample(page_history):
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


@history('word')
def test_word_diff_sample(page_history):
    scenario = (
        (u"hello", True, u"hello\n"),
        (u"world", True, u"[-hello-]{+world+}\n"
                         u"last change was 0 seconds ago"),
        (u"world", False, None),
    )
    for content, changed, report in scenario:
        result = page_history.report_changes(content)
        assert result == (changed, report)
