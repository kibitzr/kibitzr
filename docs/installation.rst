.. _install:

============
Installation
============

Stable release
--------------

To install kibitzr, run this command in your terminal:

.. code-block:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install kibitzr

This is the preferred method to install kibitzr, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Dependencies
------------

Kibitzr has many integrations and depending on what features are used may require additional setup.

The recommended way to have all dependencies installed and configured is to use `Docker`_.

Docker
------

You need a current version of `Docker present on your machine <https://docs.docker.com/install/>`_.

If you would like to run it as a service just add a ``kibitzr.yml`` file and a ``pages`` folder to your current directory and run the following command:

.. code-block:: bash

    docker run -v $PWD:/root/.config/kibitzr -v $PWD/pages:/pages peterdemin/kibitzr run

Manual installation
-------------------

The hard way is to install all dependencies.
Consult `Dockerfile`_ and :ref:`gcp` tutorial on required steps.

Kibitzr uses several Python packages, that have C extensions.
When installed through pip, they are compiling libraries.
This process requires gcc (which is almost always present)
and Python header files (which are not installed on vanilla Linux).

You can either install those dependencies use OS installer::

    apt install python-lazy-object-proxy python-yaml

or install Python headers::

    apt install python-dev

Optional dependencies
---------------------

Some of the dependencies are used only when corresponding features are used in ``kibitzr.yml``.

1. ``changes`` transform. Requires `git`_.
2. ``delay`` and ``scenario`` - triggers for using Firefox as a fetcher.
    Installing Firefox can be cumbersome, please refer to :ref:`FireFox installation guide <firefox>`.
3. HTML selectors ``xpath``, ``css`` and ``tag`` require ``lxml`` which
   compiles low-level extensions during pip installation.
   So again, you either install ``python-dev``, or install ``lxml`` from OS repo::

        apt install python-lxml

.. _Docker: https://www.docker.com/
.. _Dockerfile: https://github.com/kibitzr/kibitzr/blob/master/Dockerfile
.. _git: https://git-scm.com/
.. _xvfb: https://www.x.org/archive/X11R7.6/doc/man/man1/Xvfb.1.xhtml
