.. _configuration:

=============
Configuration
=============

.. _configuration-location:

Location
--------

``kibitzr`` reads configuration from ``kibitzr.yml`` file.
It tries to find it in following places:

1. ``./kibitzr.yml`` - current working directory.
2. ``~/.config/kibitzr/kibitzr.yml``
3. ``~/kibitzr.yml``

``kibitzr-creds.yml`` can be used to store credentials,
it must be placed in the same directory as ``kibitzr.yml``.

.. _configuration-format:

Format
------

``kibitzr`` serves list of ``checks``.

Each check may have a ``name``. If ``name`` is present it **must be unique**.
If no name is provided, it will be auto-generated.

The name is used in notifications and internally as a check identifier.

Check may have ``url``.
If it is provided, it will be used to fetch data. Optionally ``verify-cert`` can be set
to ``False`` to skip verificaiton of the SSL certificate.
Alternativelly data can be fetched by ``script``, which is an arbitrary shell script.

Check will be executed every ``period`` seconds and/or on every ``schedule``. 
See :ref:`Schedule documentation <schedule>` for a complete list of possibilities.

Fetched data from ``url`` (or ``script`` output) is passed
to a pipeline of transformations defined under ``transform`` key.
See :ref:`Transforms documentation <transforms>` for a complete list of
supported transformations.

Finally transformed data is passed to a list of notifiers
defined under ``notify`` key.
See :ref:`Notifier documentation <transforms>` for a complete list of
supported notifiers.

Kibitzr supports browser interactions. They can be activated by using any of keys:

   1. ``delay`` - number of seconds to wait after page loaded in browser to process JavaScript.
   2. ``scenario`` - python scenario acting on selenium_ driver after page load.
   3. ``form`` - shorthand for simple selenium_ scenarios.

Browser interaction is a strong side of Kibitzr and a tough article in itself.
Please refer to :ref:`Browser automation <scenario>` documentation.

.. _selenium: https://selenium-python.readthedocs.io/api.html

Environment variables
---------------------

Kibitzr provides read access to environment variables in a number of ways.

Inside :ref:`Python` scripts, use Pythonic builtin module ``os``:

.. code-block:: python

    import os
    os.environ['NAME']

In shell scripts use bash syntax:

.. code-block:: bash

    echo ${NAME}

Jinja templates have ``env`` dictionary in their context:

.. code-block:: jinja

    {{ env.NAME }}

``kibitzr-creds.yml`` supports bash-like environment interpolation provided by yamlenv_ library:

.. code-block:: yaml

    service:
        username: ${ USERNAME }
        password: ${ PASSWORD }

.. _yamlenv: https://pypi.org/project/yamlenv/

.. _configuration-example:

Example break down
------------------

Let's start with something simple. It's not very useful check, but it shows the basics.

.. code-block:: yaml

    checks:
      - name: Current Time
        url: https://www.worldtimeserver.com/current_time_in_US-NY.aspx
        transform:
          - css: "span#theTime"
          - text
        notify:
          - python: print(content)
        period: 15

Copy paste it to your ``kibitzr.yml`` and launch ``kibitzr``.
You will see something like this:

.. code-block:: bash

    $ kibitzr once
    2017-03-28 22:02:39,465 [INFO] kibitzr.checker: Fetching Current Time at https://www.worldtimeserver.com/current_time_in_US-NY.aspx
    2017-03-28 22:02:39,687 [INFO] kibitzr.notifier.custom: Executing custom notifier
    10:02:39 pm
    EDT
    2017-03-28 22:02:39,687 [INFO] kibitzr.main: Scheduling checks for 'Current Time' every 15 seconds
    2017-03-28 22:02:39,688 [INFO] kibitzr.main: Starting infinite loop
    2017-03-28 22:02:54,705 [INFO] schedule: Running job Every 15 seconds do check() (last run: [never], next run: 2017-03-28 22:02:54)
    2017-03-28 22:02:54,705 [INFO] kibitzr.checker: Fetching Current Time at https://www.worldtimeserver.com/current_time_in_US-NY.aspx
    2017-03-28 22:02:54,823 [INFO] kibitzr.notifier.custom: Executing custom notifier
    10:02:54 pm
    EDT

Let's follow the configuration file line-by-line to see how it works.

On the first line we define a dictionary key ``checks``:

.. code-block:: yaml

    checks:

Then, starting with indentation and dash goes the name of the first check:

.. code-block:: yaml

      - name: Current Time

It's an arbitrary string, the only constraint is that it must be **unique** within the ``checks`` list.

Right after name, we define URL:

.. code-block:: yaml

        url: https://www.worldtimeserver.com/current_time_in_US-NY.aspx

Please note, that all keys are in lower case.

So far so good, we came to transformations:

.. code-block:: yaml

        transform:
          - css: "span#theTime"
          - text

``transform`` value must be a list (as denoted by dashes).
Please note how list items indentation is deeper, than of ``transform``.

Each ``transform`` item can be a simple ``transform`` name (like ``text``, which extracts text from HTML),
or a ``name: argument`` pair (like ``css: "#qlook > div"`` which crops HTML using CSS selector ``"#qlook > div"``)

As you can see, we first crop whole page to a single HTML tag and then extract plain text from it.

Having all the hard job behind, we came to notification settings.
``kibitzr`` supports :ref:`many different notifiers <notifiers>`,
but here we are using the one, that does not require credentials management - arbitrary Python script.

.. code-block:: yaml

        notify:
          - python: print(content)

It is exactly the code, that produced

.. code-block:: bash

    10:02:39 pm
    EDT

in the ``kibitzr`` output.

Last line of configuration file is the ``period``:

.. code-block:: yaml

        period: 15

The number of seconds to wait between (*start of*) checks.
Kibitzr understands time to the extent, you can write ``1 hour`` instead of ``3600``.
For the more complete list of available formats refer to pytimeparse_ docs.

.. _pytimeparse: https://pypi.python.org/pypi/pytimeparse/
