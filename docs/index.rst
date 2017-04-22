=====================================
Kibitzr - Personal Network Assistant
=====================================

Kibitzr periodically runs checks desrcibed in ``kibitzr.yml`` file.
Each check has following steps:

1. Fetch page;
2. Pass it's contents through sequence of :ref:`transforms`;
3. Run set of :ref:`notifiers` with transformed content.

======================
Documentation Contents
======================

.. toctree::
   :maxdepth: 2

   installation
   configuration
   usage
   transforms
   notifiers
   python
   recipes
   contributing
