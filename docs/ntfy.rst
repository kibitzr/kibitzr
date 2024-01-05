:orphan:

.. _ntfy:

=================
Ntfy Notifier
=================

Kibitzr supports sending notifications via `ntfy service`_.

Configuration
-------------

The ntfy notifier needs an ``url`` and a ``topic`` to send notifications. You can optionally include an ``auth`` value, which will be sent in the Authorization header.

Example of ``kibitzr-creds.yml`` file:

.. code-block:: yaml

    ntfy:
        url: https://ntfy.sh
        topic: secret-topic


Now the notifier can be configured in ``kibitzr.yml`` using following syntax:

.. code-block:: yaml

    checks:
      ...
        notify:
          - ntfy


Some defaults can be overridden for each check:

.. code-block:: yaml

    checks:
      ...
        notify:
          - ntfy:
                topic: another-topic
                title: Important Notification # default: kibitzr
                priority: 5 # default: 3


.. _ntfy service: https://ntfy.sh
