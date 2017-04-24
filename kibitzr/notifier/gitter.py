from .webhook import WebHookNotify, webhook_factory


class GitterNotify(WebHookNotify):
    CREDS_KEY = 'gitter'


notify_factory = webhook_factory(GitterNotify)
