.. _notifiers:

=========
Notifiers
=========

If :ref:`transformation sequence <transforms>` produced non-empty text,
list of notifiers will be called.

Kibitzr supports following notifier types:

1. ``smtp`` - Send an e-mail through any SMTP server
2. ``mailgun`` - or send it through mailgun_ API
3. ``slack`` - Trigger `Slack Incomming Webhook`
4. ``gitter`` - Or post to gitter's chat
5. ``python`` - Run Python script
6. ``bash`` - Run bash script

Each notifier requires different configuration.
For the sake of security, sensitive information
like API tokens, usernames and passwords can (and should)
be stored in separate file - ``kibitzr-creds.yml``
It's recommended to restrict access to this file to the owner.

.. _mailgun: https://www.mailgun.com/
.. _Slack Incomming Webhook: https://api.slack.com/incoming-webhooks


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
