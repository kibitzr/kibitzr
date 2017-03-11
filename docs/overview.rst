========
Overview
========

Kibitzr periodically runs tasks desrcibed in ``kibitzr.yml`` file.
Each task has following steps:

1. Fetch page;
2. Pass it's contents through sequence of :ref:`transforms`;
3. Run set of :ref:`notifiers` with transformed content.
