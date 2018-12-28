.. _python:

==============
Python support
==============

Kibitzr check accepts Python code in 4 places:

* Script (fetcher)
* Browser automation scenario
* Transform
* Notify

Here is a simplistic example of ``kibitzr.yml`` file, that uses all three:

.. code-block:: yaml

    checks:
      - name: Python example
        script:
           python: |
                    content = "\n".join([str(x**2) for x in range(1, 4)])
        transform:
              - python: content = " ".join(reversed(content.splitlines()))
        notify:
              - python: print(content)

Once executed with debug log level it will generate following output:

.. code-block:: bash

    $ kibitzr -l debug once
    2017-04-22 10:47:04,401 [DEBUG] kibitzr.conf: Loading settings from /home/kibitzr/kibitzr.yml
    2017-04-22 10:47:04,404 [DEBUG] kibitzr.conf: Loading credentials from /home/kibitzr/kibitzr-creds.yml
    2017-04-22 10:47:04,406 [INFO] kibitzr.checker: Fetching 'Python example' using script
    2017-04-22 10:47:04,406 [INFO] kibitzr.fetcher.script: Fetch using Python script
    2017-04-22 10:47:04,406 [DEBUG] kibitzr.fetcher.script: content = "\n".join([str(x**2) for x in range(1, 4)])

    2017-04-22 10:47:04,406 [INFO] kibitzr.transformer: Python transform
    2017-04-22 10:47:04,406 [DEBUG] kibitzr.transformer: content = " ".join(reversed(content.splitlines()))
    2017-04-22 10:47:04,407 [DEBUG] kibitzr.checker: Sending report: u'9 4 1'
    2017-04-22 10:47:04,407 [INFO] kibitzr.notifier.custom: Executing custom notifier
    2017-04-22 10:47:04,407 [DEBUG] kibitzr.notifier.custom: print(content)
    9 4 1

Let's break it down.

.. _python-fetcher:

Python Fetcher
--------------

To fetch content with a script instead of URL, check must
have no ``url`` key, and have ``script`` defined.
If ``script``'s value is a string, it will be used as shell script.
Alternatively ``script`` can hold a dictionary of one item.
Item's key can be ``shell`` (for :ref:`Shell fetcher <shell>`) or ``python``.
If ``script``'s only key is ``python``, then it's value will be
executed as a Python script.
Script is an arbitrary Python code with few constraints:

1. Script can define ``ok`` boolean variable,
   which is either ``True`` or ``False``.
   When ok is ``True`` it means that content was fetched without errors.
   When ok is ``False``, content should hold error message.
   By default ``ok`` is ``True``.
2. Script must define ``content`` string variable.
   ``content`` will be passed to through ``transform`` list to ``notify`` list.
3. Script has access to check's configuration in ``conf`` global variable
   and credentials dictionary in ``creds``.

If fetching script raises an exception, the fetcher will return ``ok=False``
and ``content`` will contain full traceback.


.. _python-scenario:

Browser Automation Scenario
---------------------------

Kibitzr allows writing browser automation scenarios using Selenium_ library.
Scenario is an arbitrary Python code, which is executed after page is loaded
in the browser. Scenario has access to following global variables:

1. Check's configuration in ``conf`` global variable.
2. Credentials dictionary in ``creds``.
3. Selenium driver in ``driver``

Example scenario that authenticates in online account of Bank of America:

.. code-block:: yaml

    checks:
      - name: BofA
        url: https://www.bankofamerica.com/
        scenario: |
            login = driver.find_element_by_id("onlineId1")
            login.send_keys(creds['bofa']['login'])
            password = driver.find_element_by_id("passcode1")
            password.send_keys(creds['bofa']['password'])
            button = driver.find_element_by_id("hp-sign-in-btn")
            button.click()

Using Selenium is an advanced topic on it's own with a plenty of documentation
and many pitfalls.

.. _python-transform:

Python Transform
----------------

Python transform is similar to Python fetcher with one difference.
It accepts ``content`` variable and it puts transformed result in the same ``content`` variable.

.. code-block:: yaml

    transform:
      - python: |
          content = content.replace("election", "eating contest")


.. _python-notify:

Python Notifier
---------------

Python notify is similar to Python fetcher with one difference.
It does not return anything.


.. _python-troubleshooting:

Troubleshooting
---------------

To put break point inside Python code, just add following line:

.. code-block:: python

    import pdb; pdb.set_trace()

It will stop Kibitzr execution and start Pdb_ session.
You will have access to all variables and full execution Stack.
However, Pdb won't show current line of code, which is not convenient,
but manageable, since you know exactly where break point stands.

.. _Pdb: https://docs.python.org/3.6/library/pdb.html
.. _Selenium: https://selenium-python.readthedocs.io/
