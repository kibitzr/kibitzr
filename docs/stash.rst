.. _stash:

=====
Stash
=====

Overview
--------

Kibitzr maintains persistent key-value storage - ``stash``.
All data inside ``stash`` is accessible inside all checks
and can be referred from :ref:`python-fetcher` and :ref:`jinja transform`.

Stash keys are populated in notify.
Use ``stash`` notifier and provide it key-value dictionary.
Each value is a Jinja template.
It has access to the same context as Jinja transform.

Stored values can be printed with command:

.. code-block:: shell

    $ kibitzr stash

Example
-------

Good application for stash is checks aggregation.
Consider this news digest example:

.. code-block:: yaml

    checks:
      - url: http://www.foxnews.com/
        transform:
          - jinja: '{{ css("h1")[-1] }}'
          - text
          - jinja: '{{ lines | join(" ") }}'
        notify:
          - stash:
              fox: '{{ content }}'

      - url: https://www.nytimes.com/
        transform:
          - xpath: //*[starts-with(@id, "topnews-")]/h2/a
          - text
        notify:
          - stash:
              nytimes: '{{ content }}'

      - name: Headlines
        script:
          python: |
            content = (
              "Fox News: {0}\n"
              "NY Times: {1}"
            ).format(stash["fox"], stash["nytimes"])
        notify:
          - python: print(content)

First check, ``Fox News``, will fetch headline from foxnews.com.
Second - from nytimes.com.
They both will save headings in stash under respective keys.

Last check, ``Headlines``, uses Python script that will print something similar to:

    Fox News: LASHING OUT AT LEAKS Trump calls US disclosures in UK bombing ‘deeply troubling’
    NY Times: Trump Calls for U.S. Inquiry Into Leaks on Manchester

Implementation
--------------

Under the hood stash uses python built-in shelve module.
It stores all data in ``stash.db`` file in working directory.
Writes are atomic - if one of values fails rendering, none will be written.
