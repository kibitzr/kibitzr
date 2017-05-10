.. _credentials:

===========
Credentials
===========

It's always a good idea to store general configuration separately
from sensetive information, like usernames and password.
On the one hand, it's good from security perspective,
on the other hand it allows creating common check definitions.

Plain YAML storage
------------------

Kibitzr loads arbitrary data structures from ``kibitzr-creds.yml``
and makes it available inside transforms, fetchers and notifies through ``creds`` variable.
It's not the most secure way of storing passwords.
The good idea is to make it accessible only by owner:

.. code-block:: bash

    $ chmod 600 kibitzr-creds.yml

While it does not feel safe to store bank accounts this way,
it's a good fit for API keys (like Telegram, or Slack).

System Keyring
--------------

All modern operating systems provide some form of secure credentials storage.
But they usually require additional configuration.

Kibitzr provides access to keyrings through `python keyring`_.
To enable, install Kibitzr extension `kibitzr-keyring`_:

.. code-block:: bash

    $ pip install kibitzr-keyring

And follow the `keyring instructions`_.

Once configured, keyring values will be available in ``creds.keyring`` dictionary.

.. _`python keyring`: https://github.com/jaraco/keyring
.. _`keyring instructions`: https://github.com/jaraco/keyring#configure-your-keyring-lib
.. _kibitzr-keyring: https://pypi.python.org/pypi/kibitzr-keyring
