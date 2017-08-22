.. _SMTP:

======================================
Send notifications emails through SMTP
======================================

One of the most basic notifiers is e-mails through SMTP.
SMTP configuration has following fields:

1. ``host`` - SMTP server host name (default: ``localhost``)
2. ``port`` - SMTP server port number (default: ``25``)
3. ``user`` - User for TLS authentication, also sender (default: first recipient)
4. ``password`` - User's password if TLS authentication is on (default: ``""``)
5. ``recipients`` - list of e-mails, who will receive the notification (required)
6. ``subject`` - E-mail subject (default: check name)

First four fields (host, port, user, password) are credentials
and must be stored in ``kibitzr-creds.yml``.
Recipients and subject are defined in each check.

E-mail configuration
--------------------

Recipients list can also be just one string for brevity.
Subject can be omitted, than check's name will be used.

Following configurations are equivalent:

.. code:: yaml

    checks:
      - name: short
        ...
        notify:
          - smtp: kibitzrrr@gmail.com

      - name: middle
        ...
        notify:
          - smtp:
              - kibitzrrr@gmail.com

      - name: full
        ...
        notify:
          - smtp:
              subject: Kibitzr update for full
              recepients:
                - kibitzrrr@gmail.com


Server configuration
--------------------

Server credentials should be stored in ``kibitzr-creds.yml``.
Here is an example for Gmail:

.. code:: yaml

    smtp:
        host: smtp.gmail.com
        port: 587
        user: kibitzrrr@gmail.com
        password: (sat;hfsDA5wa@$%^jh

If there is ``smtp`` section in ``kibitzr-creds.yml``,
Kibitzr will try to use ``localhost:25``.
*From* field will be equal to first recipient.
If server authentication is turned on, password will be sent empty.
