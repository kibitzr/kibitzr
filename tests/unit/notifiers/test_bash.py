import tempfile

from kibitzr.notifier.bash import notify_factory as bash_factory


def test_bash_unicode_is_handled():
    content = u"\U0001F4A9"
    with tempfile.NamedTemporaryFile() as outfile:
        bash_notify = bash_factory({}, 'tee %s' % outfile.name)
        bash_notify(content)
        written = outfile.read().decode("utf-8")
        assert written == content


def test_bash_error_is_captured():
    bash_notify = bash_factory({}, 'command-not-found')
    bash_notify("hello")
