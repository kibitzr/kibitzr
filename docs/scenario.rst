.. _scenario:

==================
Browser automation
==================

Kibitzr uses Firefox browser and Selenium Python library for
browser automation.

Installing Firefox can be cumbersome, please refer to :ref:`FireFox installation guide <firefox>`.

Simple HTML forms can be filled using ``form`` key,
but complex scenarios require full power of Python (Selenium) scripting.

Filling simple forms
--------------------

Imagine, for example, that you need to authorize on a site
before fetching content.
For common case the check will look like:

.. code-block:: yaml

    checks:
      - name: Bank account balance
        url: https://bank.com
        form:
          - id: login
            creds: bank.login
          - id: password
            creds: bank.password
        ... (transform and notify) ...

Key ``id: login`` means that HTML element fill be found using ID selector ``login``.
Key ``creds: bank.login`` means that input's value will be taken from ``creds`` dictionary
using ``bank.login`` as a hierarchy path.
Check assumes that ``kibitzr-creds.yml`` contains:

.. code-block:: yaml

    bank:
      login: mr.robot
      password: 123&dSLHj*sdfa

Available Form Selectors
------------------------

Field can be selected using one of the three selectors: id, css, xpath.
(Make sure to use lowercase).

Available Field Value Generators
--------------------------------

As in example above, field can be filled from ``creds`` dictionary.
Another option is to provide Jinja2 template in key ``value``.
Template will have access to ``conf`` and ``creds``.
However any plain text value can be passed as well.
For example, the same value, as in creds example can be rendered by:

.. code-block:: yaml

    checks:
      - name: Bank account balance
        url: https://bank.com
        form:
          - id: login
            value: "{{ creds['bank']['login'] }}"
          - id: password
            value: "{{ creds['bank']['password'] }}"
        ... (transform and notify) ...

Note: don't forget to wrap Jinja2 template in quotes, since curly bracket
is a valid YAML markup for dictionary.
Please refer to Jinja2_ template documentation for details.


.. _Jinja2: http://jinja.pocoo.org/docs/2.9/templates/



Python scenarios with Selenium
------------------------------

For complex cases Kibitzr provides access to Selenium driver.
Here is an example of filling current date into form field:

.. code-block:: yaml

    checks:
      - name: Daily updates
        url: https://daily.com
        scenario: |
          import datetime
          today = datetime.date.today()
          element = driver.find_element_by_id('datefield-1')
          element.send_keys(today.strftime('%m/%d/%Y')
          run = driver.find_element_by_id('run-button')
          run.click()
        ... transforms and notify ...

Wait for Javascript to render contents
--------------------------------------

Sometimes web page uses some complex Javascript to render a page after it is loaded.
These pages don't require form filling, or complex scenarios, simple delay will do.
To define delay add ``delay`` key with number of seconds to wait:

.. code-block:: yaml

    checks:
      - url: https://www.producthunt.com/posts/kibitzr
        delay: 1
        ... transforms and notify ...


Working around two-factor authentication
----------------------------------------

Some sites require entering code sent in a SMS for logging from the new device.
2-FA can't be automated without weakening security.
But Kibitzr can use persistent Firefox profile.
Start persistent Firefox session with

.. code-block:: bash

    $ kibitzr firefox

Than authenticate on all sites, that require first-login 2-FA.
When ready, hit Return in the terminal prompt.
New profile will be saved in ``firefox_profile`` directory.
If this directory exists, kibitzr will load it for each following run.

Note: if running kibitzr remotely through SSH, use `X11 forwarding`_.

.. _`X11 forwarding`: <https://duckduckgo.com/?q=ssh+x11+forwarding&t=h_&ia=web>`

Debugging/Troubleshooting
-------------------------

Writing robust Selenium scenarios is no easy task, and most likely
it won't work from the first time.
Kibitzr has a few options to help with debugging.

1. See what happens in Firefox by running in foreground mode.
   Just add

   .. code-block:: yaml

       checks:
         - url: ...
           scenario:
             ...
           headless: false

   to check dictionary.

2. Launch Pdb_ within scenario and explore step-by-step.

   .. code-block:: yaml

       checks:
         - url: https://javascript-labyrinth.io
           scenario:
             import pdb; pdb.set_trace()
             ...

3. Experiment inside `Jupyter notebook`_. See `notebook example`.


.. _Pdb: https://docs.python.org/3.6/library/pdb.html
.. _`Jupyter notebook`: http://jupyter.readthedocs.io/en/latest/index.html
.. _`notebook example`: https://github.com/kibitzr/kibitzr.github.io/blob/master/Example.ipynb
