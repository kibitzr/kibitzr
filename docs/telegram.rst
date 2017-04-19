.. _telegram:

=============================
Private Telegram Bot Notifier
=============================

Kibitzr supports sending notifications through `Telegram IM`_.
Setup process consists of 3 steps:

1. Create Bot with `BotFather`_
2. Write a message (anything) to you new bot
3. Save telegram token to ``kibitzr-creds.yml``

Notes
-----

Telegram bots `don't have an ability to search for users`_,
that's why one have to write a message to bot instead of providing username in configuration.
Kibitzr will send messages to chat, where first message was sent to bot
(like `filial imprinting`_).

.. _Telegram IM: https://telegram.org/
.. _BotFather: https://telegram.me/botfather
.. _filial imprinting: https://en.wikipedia.org/wiki/Imprinting_(psychology)#Filial_imprinting
.. _don't have an ability to search for users: https://core.telegram.org/bots#4-how-are-bots-different-from-humans
