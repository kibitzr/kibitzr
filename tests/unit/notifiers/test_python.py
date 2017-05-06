import pytest

from kibitzr.notifier.factory import CompositeNotifier

from ...compat import mock
from ...helpers import SettingsMock


@pytest.fixture()
def settings():
    """Override native settings singleton with empty one"""
    return SettingsMock.instance()


def test_python_unicode_is_handled(settings):
    content = u"\U0001F4A9"
    conf = {
        'notify': [{
            'python': 'conf["content"] = content * 2',
        }],
    }
    notify_func = CompositeNotifier(conf)
    notify_func(content)
    written = conf['content']
    assert written == content * 2


@mock.patch("kibitzr.notifier.factory.logger")
def test_exception_is_captured(fake_logger):
    notify_func = CompositeNotifier({'notify': [{'python': 'print(1 / 0)'}]})
    notify_func("bang")
    fake_logger.exception.assert_called_once_with(
        "Exception occurred during sending notification"
    )
