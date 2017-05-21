import os
import logging
import tempfile
import contextlib


logger = logging.getLogger(__name__)


def execute_bash(code, stdin=None):
    if os.name == 'nt':
        executor = WindowsExecutor
    else:
        executor = BashExecutor
    return executor(code).execute(stdin)


class BashExecutor(object):

    def __init__(self, code):
        self.code = code

    def execute(self, stdin=None):
        stdin = self.prepare_input(stdin)
        with self.temp_file() as filename:
            ok, result = self.run_scipt(filename, stdin)
        return self.make_report(ok, result)

    @staticmethod
    def prepare_input(stdin):
        if stdin is not None:
            if not stdin.strip():
                logger.info("Skipping execution with empty content")
                return True, stdin
            stdin = stdin.encode("utf-8")
        return stdin

    @contextlib.contextmanager
    def temp_file(self):
        with tempfile.NamedTemporaryFile() as fp:
            logger.debug("Saving code to %r", fp.name)
            fp.write(self.code.encode('utf-8'))
            fp.flush()
            yield fp.name

    @staticmethod
    def run_scipt(name, stdin):
        from kibitzr.compat import sh
        logger.debug("Launching script %r", name)
        try:
            return True, sh.Command("bash")(name, _in=stdin)
        except sh.ErrorReturnCode as exc:
            return False, exc

    @staticmethod
    def make_report(ok, result):
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        if ok:
            log = logger.debug
            report = stdout
        else:
            log = logger.error
            report = stderr
        log("Bash exit_code: %r", result.exit_code)
        log("Bash stdout: %s", stdout)
        log("Bash stderr: %s", stderr)
        return ok, report


class WindowsExecutor(BashExecutor):

    @contextlib.contextmanager
    def temp_file(self):
        with tempfile.NamedTemporaryFile(suffix='.bat', delete=False) as fp:
            try:
                logger.debug("Saving code to %r", fp.name)
                fp.write(self.code.encode('utf-8'))
                fp.close()
                yield fp.name
            finally:
                os.remove(fp.name)

    @staticmethod
    def run_scipt(name, stdin):
        from kibitzr.compat import sh
        logger.debug("Launching script %r", name)
        try:
            return True, sh.Command("cmd.exe")("/Q", "/C", name, _in=stdin)
        except sh.ErrorReturnCode as exc:
            return False, exc

    @staticmethod
    def make_report(ok, result):
        stdout = result.stdout
        stderr = result.stderr
        if ok:
            log = logger.debug
            report = stdout
        else:
            stdout = stdout.decode('utf-8')
            stderr = stderr.decode('utf-8')
            log = logger.error
            report = stderr
        log("CMD stdout: %s", stdout)
        log("CMD stderr: %s", stderr)
        return ok, report
