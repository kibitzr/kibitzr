from __future__ import absolute_import
import logging

from .telegram import TelegramBot


logger = logging.getLogger(__name__)


class TelegramBotSplit(TelegramBot):
    def __init__(self, chat_id=None, split_on="\n"):
        self.split_on = split_on
        super(TelegramBotSplit, self).__init__(chat_id=chat_id)

    def post(self, report, **kwargs):
        """Overwrite post to split message on token"""
        for m in report.split(self.split_on):
            super(TelegramBotSplit, self).post(m)


def notify_factory(conf, value):
    try:
        chat_id = value['chat-id']
    except (TypeError, KeyError):
        chat_id = value
    try:
        split_on = value['split-on']
    except (TypeError, KeyError):
        split_on = "\n"

    return TelegramBotSplit(chat_id=chat_id, split_on=split_on).post


def chat_id():
    bot = TelegramBotSplit()
    print(bot.chat_id)
