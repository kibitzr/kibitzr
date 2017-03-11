.. _transforms:

Transforms
==========

Each Kibitzr transform modifies content and passes it forward.
Then can be divided into following groups: HTML, plain text, others.

HTML
----

1. ``tag: tagname`` - crop HTML to contents of the first matching HTML tag.
2. ``css: selector`` - crop HTML to contents of the passed `CSS selector`_.
3. ``xpath: path`` - crop HTML to contents of the passed `XPath`_.
4. ``text`` - strip all HTML tags and return only text.

Plain text
----------

1. ``changes`` - Compare to the previous version of the content and return difference report
2. ``changes: verbose`` - Same as ``changes``, but report is in human-friendly format
3. ``sort`` - Sort lines of text alphabetically
4. ``cut: N`` - Remove lines after ``N``'th

Others
------

1. ``json`` - Pretty pring JSON content (useful for APIs).

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

    pages:

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

.. _`CSS selector`: http://www.w3schools.com/cssref/css_selectors.asp
.. _`XPath`: http://www.w3schools.com/xsl/xpath_syntax.asp
