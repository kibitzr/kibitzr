====================================
Kibitzr - Personal Network Assistant
====================================

Kibitzr periodically runs checks described in ``kibitzr.yml`` file.
Each check has following steps:

1. Fetch content;
2. Pass it through sequence of :ref:`transforms`;
3. Run set of :ref:`notifiers` with transformed content.

======================
Documentation Contents
======================

.. toctree::
   :maxdepth: 2

   installation
   configuration
   credentials
   usage
   scenario
   schedule
   transforms
   notifiers
   python
   shell
   stash
   extensions
   recipes
   contributing
   contributors
   history
