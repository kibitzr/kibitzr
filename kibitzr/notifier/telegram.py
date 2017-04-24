from __future__ import absolute_import
import logging

from telegram.bot import Bot

from ..conf import settings


logger = logging.getLogger(__name__)


class TelegramBot(object):
    def __init__(self, token=None):
        if not token:
            telegram_creds = settings().creds['telegram']
            token = telegram_creds['token']
        self.bot = Bot(token=token)
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

    __call__ = post


def notify_factory(conf, value):
    return TelegramBot(value).post
