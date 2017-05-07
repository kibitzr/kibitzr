=====
Usage
=====

::

    $ kibitzr --help
    Usage: kibitzr [OPTIONS] COMMAND [ARGS]...

      Run kibitzr COMMAND --help for detailed descriptions

    Options:
      -l, --log-level [debug|info|warning|error]
                                      Logging level
      --help                          Show this message and exit.

    Commands:
      firefox  Launch Firefox with persistent profile
      init     Create boilerplate configuration files
      once     Run kibitzr checks once and exit
      run      Run kibitzr in the foreground mode
      version  Print version


CLI reads its configuration from ``kibitzr.yml`` file in current working directory.
Optionally ``kibitzr-creds.yml`` can be used to separate credentials from general configuration.

Please refer to :ref:`configuration documentation <configuration>` for ``kibitzr.yml`` format.

For commands ``run`` and ``once``
one or more ``NAME``'s can be supplied to limit
execution of configuration file to a subset of tasks.

``kibitzr`` doesn't have daemon mode. Instead it can be launched with `supervisord`_.
See :ref:`Running kibitzr as a daemon <daemon>` for details.

.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _mailgun: https://mailgun.com/
.. _slack: https://slack.com/
.. _selenium: https://selenium-python.readthedocs.io/api.html
.. _supervisord: http://supervisord.org/
