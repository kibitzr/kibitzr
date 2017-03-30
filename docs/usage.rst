=====
Usage
=====

::

	$ kibitzr --help
	Usage: kibitzr [OPTIONS] [NAME]...

	  Run kibitzr in the foreground mode

	Options:
	  --once                          Run checks once and exit
	  -l, --log-level [debug|info|warning|error]
									  Logging level
	  --help                          Show this message and exit.


CLI reads its configuration from ``kibitzr.yml`` file in current working directory.
Optionally ``kibitzr-creds.yml`` can be used to separate credentials from general configuration.

Please refer to :ref:`configuration documentation <configuration>` for ``kibitzr.yml`` format.

Optionally one or more ``NAMEs`` can be supplied to limit
execution of configuration file to a subset of tasks.

``kibitzr`` doesn't have daemon mode. Instead it can be launched with `supervisord`_.
See :ref:`Running kibitzr as a daemon <daemon>` for details.

.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _mailgun: https://mailgun.com/
.. _slack: https://slack.com/
.. _selenium: https://selenium-python.readthedocs.io/api.html
.. _supervisord: http://supervisord.org/
