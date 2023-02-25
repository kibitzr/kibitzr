import json

from .webhook import WebHookNotify, webhook_factory


class DiscordNotify(WebHookNotify):
    CREDS_KEY = 'discord'

    def configure_session(self):
        self.session.headers.update({'Content-Type': 'application/json'})

    def payload(self, report):
        return json.dumps({"content": report})


notify_factory = webhook_factory(DiscordNotify)
