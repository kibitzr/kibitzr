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

YAML file must have following structure:

1. Key ``pages`` with a list of web pages dictionaries.
   Each dictionary must have following mandatory keys:
   
   1. ``name`` - unique (in the scope of this file) user-friendly name of the web page.
   2. ``url`` - pages URL
   
   Other keys are optional:
   
   1. ``period`` - how often to check the URL for changes.
   2. ``notify`` must be a list of notifiers to use when the page is changed.
      Currently implemented notifiers are:
      
      1. ``python`` - execute any python code, having change report inside ``text`` global variable,
         page configuration in ``conf`` dictionary and credentials in ``creds``.
      2. ``bash`` - execute any bash script report is passed to stdin.
      3. ``mailgun`` - send an e-mail through mailgun_.
      4. ``slack`` - send an e-mail through slack_.

   3. ``transform`` - list of transformations to sequentially apply to page's content.
      Here are some available transformations: css, xpath, tag, text, changes, json, sort.
   4. ``delay`` - number of seconds to wait after page loaded in browser to process Javascipt.
   5. ``scenario`` - python scenario acting on selenium_ driver after page load.

2. Key ``notifiers`` must contain dictionary of notifiers configurations.

Example configuration:

.. code-block:: yaml

    pages:
    
      - name: NASA awards on preview
        url: http://preview.ncbi.nlm.nih.gov/pmc/utils/granthub/award/?authority.code=nasa&format=json
        transform:
          - json
          - changes
        period: 30
        notify:
          - mailgun
    
      - name: Rocket launches
        url: http://www.nasa.gov/centers/kennedy/launchingrockets/index.html
        transform: changes
        period: 600
        notify:
          - mailgun
    
    notifiers:
    
        # This can be moved to kibitzr-creds.yml:
        mailgun:
            key: <mailgun api key>
            domain: <your domain>
            to: <your email>

This configuration tells kibitzr to check URL at http://preview... every 5 minutes (300 seconds),
prettify JSON and compare against previously saved result. git diff output is sent through mailgun.


.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _mailgun: https://mailgun.com/
.. _slack: https://slack.com/
.. _selenium: https://selenium-python.readthedocs.io/api.html
