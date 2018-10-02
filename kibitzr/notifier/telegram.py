from __future__ import absolute_import
import logging

from ..conf import settings


logger = logging.getLogger(__name__)


class TelegramBot(object):
    def __init__(self, chat_id=None, split_on=None):
        from telegram.bot import Bot
        telegram_creds = settings().creds['telegram']
        token = telegram_creds['token']
        if chat_id is not None:
            self._chat_id = chat_id
        else:
            self._chat_id = telegram_creds.get('chat')
        self.split_on = split_on
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
        if self.split_on:
            report = report.split(self.split_on)
        else:
            report = [report]

        for r in report:
            # Telegram max message length is 4096 chars
            messages = [r[i:i + 4096] for i in range(0, len(r), 4096)]
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
    try:
        chat_id = value['chat']
    except (TypeError, KeyError):
        chat_id = value
    try:
        split_on = value['split-on']
    except (TypeError, KeyError):
        split_on = None

    return TelegramBot(chat_id=chat_id, split_on=split_on).post


def chat_id():
    bot = TelegramBot()
    print(bot.chat_id)
