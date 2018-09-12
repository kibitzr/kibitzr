.. _extensions-list:

==========
Extensions
==========

Kibitzr is built for extendability.
It uses `stevedore <https://docs.openstack.org/stevedore/latest/>`_ for loading external python libraries in preset entry points.
Official extensions live in `GitHub organization <https://github.com/kibitzr>`_.
Here is a short overview of them.

1. `kibitzr-sentry <https://github.com/kibitzr/kibitzr-sentry>`_ - send all errors and exceptions to the Sentry.
2. `kibitzr-email <https://github.com/kibitzr/kibitzr-email>`_ - make checks for incoming emails (IMAP only).
3. `kibitzr-keyring <https://github.com/kibitzr/kibitzr_keyring>`_ - use OS keyring for storing credentials.
