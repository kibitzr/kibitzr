from kibitzr.notifier.webhook import WebHookNotify

from ...compat import mock


def test_webhook_sample():
    url = 'http://localhost:0'
    notify = WebHookNotify(value=url)
    with mock.patch.object(notify.session, 'post') as fake_post:
        notify('report')
    fake_post.assert_called_once_with(
        url,
        data={'message': 'report'},
    )
