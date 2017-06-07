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


def ensure_text(text):
    if not isinstance(text, six.text_type):
        return text.decode('utf-8')
    else:
        return text
