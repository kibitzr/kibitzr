========
Overview
========


Kibitzr is a tool for reacting to changes on web pages.

It periodically polls page content and executes predefined actions when it changes.

Basic action is notification - e-mail or slack (feel free to request more),
but any python or bash script can be used instead.

It's convinient to send notifications only when something changes.
Also, while it might be not true for everyone,
text changes are apprehensible in `unified diff`_ format.

And here we come to ``changes`` - most popular Kibitzr transform.
It compares current page content with previous (stored in local git_ repository)
and outputs difference.

There are a lot of other transforms available and it is easy to write your own.

For example, ``text`` transform strips tags from HTML leaving only plain text.
``css`` and ``xpath`` transforms crop page to one HTML element using `CSS selectors`_
and `XPath`_ queries.

Kibitzr can be represented as following sequence of actions:

1. Fetch page;
2. Pass it's content through sequence of transforms;
3. Run set of notifiers with transformed content.


.. _`unified diff`: https://en.wikipedia.org/wiki/Diff_utility#Unified_format
.. _git: https://git-scm.com/
.. _`CSS selectors`: http://www.w3schools.com/cssref/css_selectors.asp
.. _`XPath`: http://www.w3schools.com/xsl/xpath_syntax.asp
