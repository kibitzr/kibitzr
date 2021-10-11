.. _gotify:

=================
Gotify Notifier
=================

Kibitzr supports sending notifications via `Gotify service`_.

Configuration
-------------

The Gotify notifier needs an ``url`` and an application ``token`` to send notifications.

Example of ``kibitzr-creds.yml`` file:

.. code-block:: yaml

    gotify:
        url: https://gotify.example.net/
        token: A0dIInnCs1J1zNN


Now the notifier can be configured in ``kibitzr.yml`` using following syntax:

.. code-block:: yaml

    checks:
      ...
        notify:
          - gotify


Some defaults can be overridden for each check:

.. code-block:: yaml

    checks:
      ...
        notify:
          - gotify:
                title: Important Notification # default: kibitzr
                priority: 7 # default: 4


The request to the Gotify server performs an SSL certificate verification.
If you are **aware of the implications** and still want to bypass this verification,
you can do that by adding a ``verify: false`` flag to the configuration:

.. code-block:: yaml

    gotify:
        url: https://gotify.example.net/
        token: A0dIInnCs1J1zNN
        verify: false


.. _Gotify service: https://gotify.net/
