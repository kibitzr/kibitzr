import unittest
import tempfile
import shutil
from kibitzr.storage import PageHistory


class PageHistoryTestCase(unittest.TestCase):
    def setUp(self):
        self.storage_dir = tempfile.mkdtemp()
        self.history = PageHistory(
            conf={'name': 'test', 'url': 'web'},
            storage_dir=self.storage_dir,
        )

    def tearDown(self):
        shutil.rmtree(self.storage_dir)

    def test_unified_diff_sample(self):
        scenario = (
            (u"hello", True, u"@@ -0,0 +1 @@\n+hello"),
            (u"world", True, u"@@ -1 +1 @@\n-hello\n+world"),
            (u"world", False, None),
        )
        for content, changed, report in scenario:
            result = self.history.report_changes(content, verbose=False)
            assert result == (changed, report)

    def test_verbose_diff_sample(self):
        scenario = (
            (u"hello", True, u"hello"),
            (u"world", True, u"Previous value:\nhello\nNew value:\nworld\n"),
            (u"world", False, None),
        )
        for content, changed, report in scenario:
            result = self.history.report_changes(content, verbose=True)
            assert result == (changed, report)
