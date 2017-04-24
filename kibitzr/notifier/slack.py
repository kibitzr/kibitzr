import json

from .webhook import WebHookNotify, webhook_factory


class SlackNotify(WebHookNotify):
    CREDS_KEY = 'slack'

    def payload(self, report):
        return json.dumps({"text": report})


notify_factory = webhook_factory(SlackNotify)
