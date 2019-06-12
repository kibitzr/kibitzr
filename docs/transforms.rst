.. _transforms:

Transforms
==========

Each Kibitzr transform modifies content and passes it forward.
Transforms can be divided into following groups: HTML, plain text, JSON.

HTML
----

* ``tag: tagname`` - crop HTML to contents of the first matching HTML tag.
* ``css: selector`` - crop HTML to the first encountered outer HTML matching passed `CSS selector`_.
* ``css-all: selector`` - crop HTML to the concatenated list of all matching elements.
* ``xpath: path`` - crop HTML to contents of the passed `XPath`_.
* ``xpath-all: path`` - crop HTML to the concatenated list of all matching elements.
* ``text`` - strip all HTML tags and return only text.

Plain text
----------

* ``changes`` - Compare to the previous version of the content and return difference report.
* ``changes: verbose`` - Same as ``changes``, but in human-friendly format.
* ``changes: word`` - Same as ``changes``, but highlight changes within a string.
* ``jinja: template`` - Render Jinja2 template. See `jinja transform`_ for reference.  

Code
----

* ``python: code`` - Execute arbitrary :ref:`Python *code* <python>` on passed content.
* ``shell: code`` - Execute arbitrary :ref:`shell` *code* on passed content. Call ``grep``, ``awk`` or ``sed``, for example.

JSON
----

* ``json`` - Pretty print JSON content.
* ``jq`` - Apply jq JSON transformation (`jq`_ must be installed).

.. _jinja transform:

Jinja Transform
---------------

Kibitzr supports Jinja2_ templates.
Following variables are passed into a context:

* ``conf`` - check configuration dictionary
* ``stash`` - global persistent key-value storage; See :ref:`stash` for details
* ``content`` - input as plain text
* ``lines`` - input as a list of lines
* ``json`` - input parsed from JSON
* ``css`` - crop input HTML to CSS selector, similar to ``css-all`` transform
* ``xpath`` - crop input XML to XPath selector, similar to ``xpath`` transform
* ``env`` - environment variables dictionary.

Also set of built-in Jinja filters is extended with:

* ``text`` - strip all HTML tags and return only text
* ``float`` - remove all characters except numbers and point.
* ``int`` - convert text or float to integer

Because Jinja transform uses general-purpose template engine, it can supersede simpler transforms.
However greater powers come with more points of failure.
Debugging of failed Jinja2 template might be challenging.
Generally I recommend using it only if you can't achieve desired effect without it.

Examples
--------

Here is a sequence of transformations, that will

1. Crop HTML page to CSS selector ``#plugin-description > div > p > a``
2. Transform it's contents to text
3. Compare it to previous value and report difference in human-readable form.

.. code-block:: yaml

    - css: "#plugin-description > div > p > a"
    - text
    - changes: verbose

Complete ``kibitzr.yml`` could look like this:

.. code-block:: yaml

    checks:
      - name: JetPack updates
        url: https://wordpress.org/plugins/jetpack/
        transform:
          - css: "#plugin-description > div > p > a"
          - text
          - changes: verbose
        notify:
          - smtp: me@gmail.com
        period: 3600

When launched first time, it will send e-mail to me@gmail.com with contents::

    Download Version 4.6

Once page contents changes, on next kibitzr launch the e-mail will be::

    Previous value:
    Download Version 4.6
    New value:
    Download Version 4.7

Next config will notify on new Kibitzr releases published on GitHub:

.. code-block:: yaml

    checks:
      - name: Kibitzr releases
        url: https://api.github.com/repos/kibitzr/kibitzr/releases
        transform:
          - jq: ".[] | .tag_name + \" \" + .name"
          - changes
        notify:
          - slack
        period: 3600

Example Slack message::

    @@ -1,2 +1,3 @@
    + "v2.6.2 Added jq transformer"
      "2.6.1 Fixed git repo configuration"
      "2.6.0 Added \"changes: verbose\" transformer"


.. _`CSS selector`: http://www.w3schools.com/cssref/css_selectors.asp
.. _`XPath`: http://www.w3schools.com/xsl/xpath_syntax.asp
.. _`jq`: https://stedolan.github.io/jq/
.. _Jinja2: http://jinja.pocoo.org/
