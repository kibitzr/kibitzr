from .webhook import WebHookNotify, webhook_factory


class ZapierNotify(WebHookNotify):
    CREDS_KEY = "zapier"
    POST_KEY = "text"

    def configure_session(self):
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded"
        })


notify_factory = webhook_factory(ZapierNotify)
