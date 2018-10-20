.. _schedule:

========
Schedule
========

Kibitzr checks are scheduled to run according to the ``period`` and ``schedule`` configuration options.
When no ``period`` or ``schedule`` is defined, a check has the default period of 5 minutes.

Keep in mind that Kibitzr runs checks sequentially, so there is no guarantee on the precise start time of a check, one long-running check delays the next one.

.. _schedule-period:

Period
------
The number of seconds to wait between (start of) checks. The ``period`` option can handle any of the formats supported by pytimeparse_ (e.g., 37 minutes, 2 hours)

.. code-block:: yaml

    checks:
      - name: Current Time
        ...
        period: 15

      - name: Fancy check
        ...
        period: 2 hours

.. _schedule-schedule:

Schedule
--------
``schedule`` option provides finer control over start time, it can be set as a single item or as a list of items.
A check runs for each ``schedule`` item configured.

The syntax is:

 * ``every`` (integer) - interval length, required;
 * ``unit`` (string) - unit of the interval;
 * ``at`` (string) - time to run the check in HH:MM format. Applicable only if unit is "days".

The rule mimics the pattern: "Every ``every`` ``unit`` at ``at``."

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

``unit`` is one of ``seconds``, ``minutes``, ``hours``, ``days`` or ``weeks``.
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
        - every: day
          at: "15:30"
        - every: hour
        - every: saturday
          at: "12:13"

For a detailed list of scheduling options, see `schedule documentation`_ which powers the Kibitzr scheduler.

.. _schedule documentation: https://schedule.readthedocs.io/en/stable/
.. _pytimeparse: https://pypi.python.org/pypi/pytimeparse/
