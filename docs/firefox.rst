.. _firefox:

==================
Installing FireFox
==================

Installing Firefox can be cumbersome.
First, you'll need `xvfb`_ to run FireFox in headless mode::

    apt install xvfb firefox

Modern FireFox
--------------

If FireFox version is greater than **52**, it will require additional binary - geckodriver.
It's not available in OS repositories and must be downloaded from `this page`_.
Simple untar the binary to ``/usr/local/bin`` or ``~/bin/`` - it must be on ``PATH`` environment variable.

Old FireFox
-----------

Having FireFox version less than **52** is easier in setup.
But you have to stick to the old version of `selenium`_ python package:

.. code-block:: console

    $ pip install 'selenium<3.0'

.. _`this page`: https://github.com/mozilla/geckodriver/releases/
.. _`selenium`: http://www.seleniumhq.org/
