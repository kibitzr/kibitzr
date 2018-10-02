.. _telegram:

=================
Telegram Notifier
=================

Kibitzr supports sending notifications through `Telegram IM`_.
Setup process consists of 4 steps:

1. Create Bot with `BotFather`_
2. Save telegram token to ``kibitzr-creds.yml``
3. Write a message (anything) to you new bot
4. Run ``kibitzr telegram_chat``
5. Save the result to ``kibitzr-creds.yml``

Configuration
-------------

Telegram bots `don't have an ability to search for users`_,
that's why one have to write a message to bot instead of providing username in configuration.
Also, bots have a short memory. Message sent a week ago will be likely inaccessible for a bot.
That's why, you have to save chat id explicitly.
Kibitzr will send messages to chat, where first message was sent to bot
(like `filial imprinting`_).

Telegram has a `maximum message length of 4096 utf-8 characters`_. Telegram Notifier will 
check this for you and split the message in to multiple messages of 4096 characters each. 
This mechanism is a fail-safe to deliver your message even when it's over the limit. When
planning on often sending larger message consider using option ``split-on``.
Messages doesn't necessarely get delivered, by the telegram network, in the same order 
that they are sent because of it async nature.

Example of ``kibitzr-creds.yml`` file:

.. code-block:: yaml

    telegram:
        token: 334539109:ABHCRz_snz8554qsSlIIotMaNFWB3p8P84
        chat: 118860645


Also chat identifier can be configured for each check in ``kibitzr.yml`` using following syntax:

.. code-block:: yaml

    checks:
      ...
        notify:
          - telegram: 118860645


Optionally can be configured to split in to multiple messages by setting ``split-on``:

.. code-block:: yaml

    checks:
      ...
        notify:
          - telegram: 
            chat: 118860645
            split-on: "\n"


.. _Telegram IM: https://telegram.org/
.. _BotFather: https://telegram.me/botfather
.. _filial imprinting: https://en.wikipedia.org/wiki/Imprinting_(psychology)#Filial_imprinting
.. _don't have an ability to search for users: https://core.telegram.org/bots#4-how-are-bots-different-from-humans
.. _maximum message length of 4096 utf-8 characters: https://core.telegram.org/method/messages.sendMessage
