=====
Usage
=====

::

    kibitzer [OPTIONS]
    
    Options:
      --once                          Run checks once and exit
      -l, --log-level [debug|info|warning|error]
                                      Logging level
      --help                          Show this message and exit.


CLI reads its configuration from ``kibitzer.yml`` file in current working directory.

YAML file must have following structure:

1. Key ``pages`` with a list of web pages dictionaries.
   Each dictionary must have following mandatory keys:
   
   1. ``name`` - unique (in the scope of this file) user-friendly name of the web page.
   2. ``url`` - pages URL
   
   Other keys are optional:
   
   1. ``format`` - page contents format for reporting changes.
      May be one of: html, text, json, asis.
      ``json`` and ``asis`` formats are using requests_.get query and,
      while being useful for simple HTTP(s) requests,
      don't provide great flexibility.
      ``html`` format uses FireFox browser to open given ``url``,
      then it delays for ``delay`` seconds to make sure all Javascript finished loading,
      then it finds first ``tag`` or ``xpath`` on loaded page,
      and returns it's contents.
      ``text`` format is the same as ``html`` but before returning, HTML is converted
      to plain text using BeautifulSoup_ library.
   2. ``period`` - how often to check the URL for changes.
   3. ``notify`` must be a list of notifiers to use when the page is changed.
      Currently implemented notifiers are:
      1. ``python`` - execute any python code, having change report inside ``text`` global variable.
      2. ``mailgun`` - send an e-mail through mailgun_.

2. Key ``notifiers`` must contain dictionary of notifiers configurations.

Example configuration:

.. code-block:: yaml

    pages:
    
      - name: NASA awards on preview
        url: http://preview.ncbi.nlm.nih.gov/pmc/utils/granthub/award/?authority.code=nasa&format=json
        format: json
        period: 30
        notify:
          - mailgun
    
      - name: Rocket launches
        url: http://www.nasa.gov/centers/kennedy/launchingrockets/index.html
        format: text
        period: 600
        notify:
          - mailgun
    
    notifiers:
    
        mailgun:
            key: <mailgun api key>
            domain: <your domain>
            to: <your email>

This configuration tells kibitzer to check URL at http://preview... every 5 minutes (300 seconds)


.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _mailgun: https://mailgun.com/
