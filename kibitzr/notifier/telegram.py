from __future__ import absolute_import
import logging

from ..conf import settings


logger = logging.getLogger(__name__)


class TelegramBot(object):
    def __init__(self, chat_id=None):
        from telegram.bot import Bot
        telegram_creds = settings().creds['telegram']
        token = telegram_creds['token']
        if chat_id is not None:
            self._chat_id = chat_id
        else:
            self._chat_id = telegram_creds.get('chat')
        self.bot = Bot(token=token)

    @property
    def chat_id(self):
        if self._chat_id is None:
            chat = self.bot.getUpdates(limit=1)[0].message.chat
            logger.debug("Imprinted chat id %d of type %s",
                         chat.id, chat.type)
            self._chat_id = chat.id
        return self._chat_id

    def post(self, report, **kwargs):
        # Telegram max message length is 4096 utf chars
        messages = [report[i:i + 4096] for i in range(0, len(report), 4096)]
        for m in messages:
            self.send_message(m)

    def send_message(self, message):
        message = self.bot.send_message(
            self.chat_id,
            message,
            parse_mode='Markdown',
        )
        return message

    __call__ = post


def notify_factory(conf, value):
    return TelegramBot(value).post


def chat_id():
    bot = TelegramBot()
    print(bot.chat_id)
