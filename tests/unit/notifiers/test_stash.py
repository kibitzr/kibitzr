from kibitzr.notifier import notify_factory

from ...helpers import stash_mock


def make_stash(**kwargs):
    return notify_factory({'notify': [{'stash': dict(**kwargs)}]})


def test_stash_is_persistent():
    with stash_mock() as stash:
        notifier = make_stash(key='{{content}}')
        notifier.notify('test')
        assert stash.read() == {'key': 'test'}
