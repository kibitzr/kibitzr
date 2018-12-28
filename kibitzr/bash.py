"""
Kibitzr accepts shell scripts in 3 places:

* Fetch
* Transform
* Notify

Execute code from notifier with transformation result passed via stdin.

Here is a simplistic example of ``kibitzr.yml`` file, that uses all three:

.. code-block:: yaml

    checks:
      - name: Shell example
        script: |
          for i in seq 1 3
          do
              echo "Number $i"
          done
        transform:
          - shell: grep 2
        notify:
          - shell: tac

Let's break it down.

.. _shell-fetcher:

Shell Fetcher
-------------

If ``script``'s value is a string, it will be used as shell script.
Alternatively ``script`` can hold a dictionary of one item.
Item's key can be ``shell`` (or ``python`` for :ref:`Python fetcher <python>`).
If ``script``'s only key is ``shell``, then it's value will be
executed as a Shell script.
Under Linux, executor is ``bash``, under Windows - ``cmd.exe``.
Script is an arbitrary shell code. It's output will be passed to transforms.
If exit code is not zero, check will be aborted.
Shell scripts don't have access to credentials, but inherit Kibitzr environment.

Shell Transform and Notifier
----------------------------

Transform and notifier are similar to fetcher. Except that they receive content via stdin,
and notifier's stdout is ignored.

Example
-------

Returning to the example, execution will go as follows:

.. code-block:: bash

    [DEBUG] kibitzr.conf: Loading settings from /home/deminp/kibitzr/tmp/kibitzr.yml
    [INFO] kibitzr.fetcher.loader: Fetching 'Shell' using script
    [DEBUG] kibitzr.bash: Saving code to '/tmp/tmpTTPSxA.bat'
    [DEBUG] kibitzr.bash: Launching script '/tmp/tmpTTPSxA.bat'
    [DEBUG] kibitzr.bash: Command exit code: 0
    [DEBUG] kibitzr.bash: Command stdout: Number 1
    Number 2
    Number 3

    [DEBUG] kibitzr.bash: Command stderr:
    [DEBUG] kibitzr.bash: Saving code to '/tmp/tmpV4Grg8.bat'
    [DEBUG] kibitzr.bash: Launching script '/tmp/tmpV4Grg8.bat'
    [DEBUG] kibitzr.bash: Command exit code: 0
    [DEBUG] kibitzr.bash: Command stdout: Number 2
    [DEBUG] kibitzr.bash: Command stderr:
    [DEBUG] kibitzr.notifier.factory: Sending report: u'Number 2'
    [DEBUG] kibitzr.bash: Saving code to '/tmp/tmpm6sRVx.bat'
    [DEBUG] kibitzr.bash: Launching script '/tmp/tmpm6sRVx.bat'
    [DEBUG] kibitzr.bash: Command exit code: 0
    [DEBUG] kibitzr.bash: Command stdout: 2 rebmuN
    [DEBUG] kibitzr.bash: Command stderr:

Fetcher script produced output:

.. code-block:: bash

    Number 1
    Number 2
    Number 3

Shell transform filtered lines that contain 2:

.. code-block:: bash

    Number 2

Notifier echoed reversed line:

.. code-block:: bash

    2 rebmuN

Notifier's stdout is ignored, so we don't see it along Kibitzr output.

And here is what happens when shell script produces error:

.. code-block:: bash

    $ cat kibitzr.yml
    checks:
      - name: Shell
        script: ls /non-existing
        notify:
          - shell: rev

    $ kibitzr -l debug once
    [DEBUG] kibitzr.conf: Loading settings from /home/deminp/kibitzr/tmp/kibitzr.yml
    [INFO] kibitzr.fetcher.loader: Fetching 'Shell' using script
    [DEBUG] kibitzr.bash: Saving code to '/tmp/tmpyNakOP.bat'
    [DEBUG] kibitzr.bash: Launching script '/tmp/tmpyNakOP.bat'
    [ERROR] kibitzr.bash: Command exit code: 2
    [ERROR] kibitzr.bash: Command stdout:
    [ERROR] kibitzr.bash: Command stderr: ls: cannot access '/non-existing': No such file or directory
    [DEBUG] kibitzr.transformer.factory: Notifying on error
    [DEBUG] kibitzr.notifier.factory: Sending report: u"ls: cannot access '/non-existing': No such file or directory"
    [DEBUG] kibitzr.bash: Saving code to '/tmp/tmpqdZwKI.bat'
    [DEBUG] kibitzr.bash: Launching script '/tmp/tmpqdZwKI.bat'
    [DEBUG] kibitzr.bash: Command exit code: 0
    [DEBUG] kibitzr.bash: Command stdout: yrotcerid ro elif hcus oN :'gnitsixe-non/' ssecca tonnac :sl
    [DEBUG] kibitzr.bash: Command stderr:
"""
import os
import logging
import tempfile
import contextlib

import six


logger = logging.getLogger(__name__)


def execute_bash(code, stdin=None):
    if os.name == 'nt':
        executor = WindowsExecutor
    else:
        executor = BashExecutor
    return executor(code).execute(stdin)


class BashExecutor(object):

    EXECUTABLE = "bash"
    ARGS = []

    def __init__(self, code):
        self.code = code

    def execute(self, stdin=None):
        if stdin is not None and stdin.strip():
            stdin = stdin.encode("utf-8")
            with self.temp_file() as filename:
                ok, result = self.run_scipt(filename, stdin)
            return self.make_report(ok, result)
        else:
            logger.info("Skipping execution with empty content")
            return True, stdin

    @contextlib.contextmanager
    def temp_file(self):
        """
        Create temporary file with code and yield its path.
        Works both on Windows and Linux
        """
        with tempfile.NamedTemporaryFile(suffix='.bat', delete=False) as fp:
            try:
                logger.debug("Saving code to %r", fp.name)
                fp.write(self.code.encode('utf-8'))
                fp.close()
                yield fp.name
            finally:
                os.remove(fp.name)

    @classmethod
    def run_scipt(cls, name, stdin):
        from kibitzr.compat import sh
        logger.debug("Launching script %r", name)
        try:
            args = cls.ARGS + [name]
            return True, sh.Command(cls.EXECUTABLE)(*args, _in=stdin)
        except sh.ErrorReturnCode as exc:
            return False, exc

    @staticmethod
    def make_report(ok, result):
        stdout = ensure_text(result.stdout)
        stderr = ensure_text(result.stderr)
        if ok:
            log = logger.debug
            report = stdout
        else:
            log = logger.error
            report = stderr
        if hasattr(result, 'exit_code'):
            log("Command exit code: %r", result.exit_code)
        log("Command stdout: %s", stdout)
        log("Command stderr: %s", stderr)
        return ok, report


class WindowsExecutor(BashExecutor):

    EXECUTABLE = "cmd.exe"
    ARGS = ["/Q", "/C"]

    @classmethod
    def run_scipt(cls, name, stdin):
        return BashExecutor.run_scipt(
            name,
            stdin.decode("utf-8"),
        )


def ensure_text(text):
    if not isinstance(text, six.text_type):
        return text.decode('utf-8')
    else:
        return text
