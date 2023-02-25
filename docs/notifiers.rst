.. _notifiers:

=========
Notifiers
=========

If :ref:`transformation sequence <transforms>` produced non-empty text,
list of notifiers will be called.

Kibitzr supports following notifier types:

1. ``smtp`` - Send an e-mail through any SMTP server; See :ref:`SMTP notifier docs <SMTP>` for details
2. ``mailgun`` - or send it through mailgun_ API
3. ``slack`` - Trigger `Slack Incoming Webhook`_
4. ``telegram`` - Send message through :ref:`private Telegram Bot <telegram>`
5. ``zapier`` - Trigger `Zapier Catch Hook`_
6. ``gitter`` - Post to gitter's chat
7. ``gotify`` - Push notification via :ref:`Gotify <gotify>`
8. ``python`` - Run :ref:`Python script <python>`
9. ``shell`` - Run :ref:`shell script <shell>`
10. ``stash`` - Save to persistent global key-value storage; See :ref:`stash` for details
11. ``discord`` - Trigger Discord's webhook
12. ``twilio`` - Send SMS through Twilio client 

Each notifier requires different configuration.
For the sake of security, sensitive information
like API tokens, usernames and passwords can (and should)
be stored in separate file - ``kibitzr-creds.yml``
It's recommended to restrict access to this file to the owner.

.. _mailgun: https://www.mailgun.com/
.. _Slack Incoming Webhook: https://api.slack.com/incoming-webhooks
.. _Zapier Catch Hook: https://zapier.com/developer/documentation/v2/static-webhooks/


Example configurations
----------------------

.. code:: yaml

    smtp:
        host: smtp.gmail.com
        port: 587
        user: kibitzrrr@gmail.com
        password: (sat;hfsDA5wa@$%^jh

    mailgun:
        key: key-asdkljdiytjk89038247102380
        domain: sandbox57895483457894350345.mailgun.org
        to: John Doe <john.doe@gmail.com>

    slack:
        url: https://hooks.slack.com/services/T5665TUV/B21J7KCTX/Ov2xUt84atxi4yjvBnEqMIKX

    gitter:
        url: https://webhooks.gitter.im/e/24a1042f49211ca9504a

    telegram:
        token: 343558405:ABHCRh_rnzO554skSlISotUnNFWt3p8P004

    zapier:
        url: https://hooks.zapier.com/hooks/catch/1670195/9asu13/

    gotify:
        url: https://gotify.example.de/
        token: A0dIInnCs1J1zNN

    discord:
        url: https://discord.com/api/webhooks/1234567890123456789/qwertyu1pQWER3YUOP_qw4rtyuo6QWER8YU-qwe9tyuopQ1ERTY2OPqw3rtyu-4werty

    twilio:
        account_sid: "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        auth_token: "your_auth_token"
