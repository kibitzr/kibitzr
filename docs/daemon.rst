.. _daemon:

===================
Running as a daemon
===================

Recommended way of daemonizing kibitzr is by using `supervisord`_.

You can install supervisord along with the kibitzr by running:

.. code-block:: bash

    $ pip install supervisord

Here is an example configuration to get you up and running:

.. code-block:: ini

    [unix_http_server]
    file=%(here)s/supervisor.sock

    [supervisord]
    logfile=%(here)s/supervisord.log
    logfile_maxbytes=50MB
    logfile_backups=10
    loglevel=info
    pidfile=%(here)s/supervisord.pid
    nodaemon=false
    minfds=1024
    minprocs=200

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=unix:///%(here)s/supervisor.sock

    [program:kibitzr]
    command=kibitzr run
    directory=%(here)s
    startsecs=30
    stopwaitsecs=600
    stderr_logfile=%(here)s/logs/kibitzr.log
    stderr_logfile_maxbytes=10MB
    stderr_logfile_backups=10
    stderr_capture_maxbytes=1MB

Just make sure, that ``logs`` directory exists and is writable.

Having this configuration in `supervisor.ini`, launch using command:

.. code-block:: bash
    
    $ supervisord -c supervisor.ini

Later you can inspect kibitzr status with

.. code-block:: bash
    
    $ supervisorctl -c supervisor.ini status

(Note that another executable is used: supervisorctl instead of supervisord)

Or shut down kibitzr it with:

.. code-block:: bash
    
    $ supervisorctl -c supervisor.ini stop kibitzr

.. _supervisord: http://supervisord.org/
