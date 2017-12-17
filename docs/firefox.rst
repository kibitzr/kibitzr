.. _firefox:

==================
Installing FireFox
==================

Firefox brings Kibitzr capabilities to the whole new level.
In the old days installing Firefox was cumbersome. But since version 56 it's no longer the case.
Firefox has special helper binary, that allows automating browser tasks.
It's called `geckodriver`_. On the upside, it generally works fine.
On the downside, it's early beta and it's not yet available in OS repositories
and must be downloaded from `this page`_.

Unpack the binary and move it to ``/usr/local/bin`` or ``~/bin/``.
Also you can just add directory with binary to the ``PATH`` environment variable.

.. _`this page`: https://github.com/mozilla/geckodriver/releases/
.. _`geckodriver`: https://github.com/mozilla/geckodriver/
.. _`selenium`: http://www.seleniumhq.org/