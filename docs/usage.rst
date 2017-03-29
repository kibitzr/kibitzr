=====
Usage
=====

::

    kibitzr [OPTIONS]
    
    Options:
      --once                          Run checks once and exit
      -l, --log-level [debug|info|warning|error]
                                      Logging level
      --help                          Show this message and exit.


CLI reads its configuration from ``kibitzr.yml`` file in current working directory.
Optionally ``kibitzr-creds.yml`` can be used to separate credentials from general configuration.

Please refer to :ref:`configuration documentation <configuration>` for ``kibitzr.yml`` format.

.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _mailgun: https://mailgun.com/
.. _slack: https://slack.com/
.. _selenium: https://selenium-python.readthedocs.io/api.html
