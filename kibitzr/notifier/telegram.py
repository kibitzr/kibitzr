from __future__ import absolute_import
import logging

from lazy_object_proxy import Proxy as Lazy
from telegram.bot import Bot

from ..conf import settings


logger = logging.getLogger(__name__)


class TelegramBot(object):
    def __init__(self, *args, **kwargs):
        telegram_creds = settings().notifiers.get('telegram', {})
        telegram_creds.update(settings().creds.get('telegram', {}))
        self.bot = Bot(token=telegram_creds['token'])
        self._chat_id = None

    @property
    def chat_id(self):
        if self._chat_id is None:
            chat = self.bot.getUpdates(limit=1)[0].message.chat
            logger.debug("Imprinted chat id %d of type %s",
                         chat.id, chat.type)
            self._chat_id = chat.id
        return self._chat_id

    def post(self, report, **kwargs):
        message = self.bot.send_message(self.chat_id, report)
        return message
