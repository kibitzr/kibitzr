.. _schedule:

========
Schedule
========

Kibitzr checks are scheduled to run according to the ``period`` and ``schedule`` configuration options.
When no ``period`` nor ``schedule`` is defined, a default period of 5 minutes will be used.

Keep in mind that Kibitzr checks are run sequentially, so there is no garantee on the precise run time of a check.

.. _schedule-period:

Period
------
The number of seconds to wait between (start of) checks. The ``period`` option can handle any of the formats supported by pytimeparse_.

.. code-block:: yaml

    checks:
      - name: Current Time
        ...
        period: 15

      - name: Fancy check
        ...
        period: 2 hours

.. _schedule-period:

Schedule
--------
For a more detailed scheduling of a check, the ``schedule`` option is available, it can be set as a single item or as a list of items. 
A check will be setup to run for each ``schedule`` item configured. So one can mix as necessary.

The syntax is:

 * ``every``: defines the period
 * ``unit``: defines the unit of the period
 * ``at``: only when is scheduled to run every N days, it can be used to specify the time

.. code-block:: yaml
    
    checks:
      ...
      schedule:
         every: 1
         unit: days
         at: "12:00"

      ...
      schedule:
         every: 1
         unit: hours


``unit`` is one of ``seconds``, ``minutes``, ``hours``, ``days`` or ``weeks`` 
When ``every`` is set to ``1`` it can be condensed with the single version of the ``unit``:

.. code-block:: yaml
    
    checks:
      ...
      schedule:
         every: day
         at: "12:00"

      
Optionally, ``every`` can also be one of ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday`` or ``sunday``.

.. code-block:: yaml
    
    checks:
      ...
      schedule:
         every: thursday
         at: "12:00"


Examples
--------

.. code-block:: yaml

    checks
      - name: Late alarm
        ...
        schedule:
          every: 1
          unit: day
          at: "20:30"

      - name: Crazy scheduling
        ...
        schedule:
        - every: 1
          unit: day
          at: "15:30"
        - every: hour
        - every: saturday
          at: "12:00"

For a detailed list of scheduling options, see `schedule documentation`_ wich powers the Kibitzr scheduler.

.. _schedule documentation: https://schedule.readthedocs.io/en/stable/
.. _pytimeparse: https://pypi.python.org/pypi/pytimeparse/
