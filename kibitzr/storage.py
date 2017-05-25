import os
import itertools
import io

from kibitzr.compat import sh

from .utils import normalize_filename


def report_changes(conf, content):
    return PageHistory(conf).report_changes(content)


class PageHistory(object):
    """
    Single file changes history using git
    """
    STORAGE_DIR = "pages"

    def __init__(self, conf, storage_dir=None, style=None):
        self.storage_dir = storage_dir or self.STORAGE_DIR
        self.cwd = os.path.join(
            self.storage_dir,
            normalize_filename(conf['name']),
        )
        self.target = os.path.join(self.cwd, "content")
        self.git = sh.Command('git').bake(
            '--no-pager',
            _cwd=self.cwd,
        )
        self.ensure_repo_exists()
        if conf.get('url'):
            self.commit_msg = u"{name} at {url}".format(
                name=conf['name'],
                url=conf.get('url'),
            )
        else:
            self.commit_msg = conf['name']
        self.reporter = ChangesReporter(
            self.git,
            self.commit_msg,
            style,
        )

    def report_changes(self, content):
        """
        1) Write changes in file,
        2) Commit changes in git
        3.1) If something changed, return tuple(True, changes)
        3.2) If nothing changed, return tuple(False, None)
        If style is "verbose", return changes in human-friendly format,
        else use unified diff
        """
        self.write(content)
        if self.commit():
            return True, self.reporter.report()
        else:
            return False, None

    def write(self, content):
        """Save content on disk"""
        with io.open(self.target, 'w', encoding='utf-8') as fp:
            fp.write(content)
            if not content.endswith(u'\n'):
                fp.write(u'\n')

    def commit(self):
        """git commit and return whether there were changes"""
        self.git.add('-A', '.')
        try:
            self.git.commit('-m', self.commit_msg)
            return True
        except sh.ErrorReturnCode_1:
            return False

    def ensure_repo_exists(self):
        """Create git repo if one does not exist yet"""
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)
        if not os.path.isdir(os.path.join(self.cwd, ".git")):
            self.git.init()
            self.git.config("user.email", "you@example.com")
            self.git.config("user.name", "Your Name")


class ChangesReporter(object):

    def __init__(self, git, subject, style=None):
        self.git = git
        self.subject = subject
        self.report = getattr(self, style or 'default', self.default)

    def word(self):
        """Return last changes with word diff"""
        try:
            output = self.git.diff(
                '--no-color',
                '--word-diff=plain',
                'HEAD~1:content',
                'HEAD:content',
            ).stdout.decode('utf-8')
        except sh.ErrorReturnCode_128:
            result = self.git.show(
                "HEAD:content").stdout.decode("utf-8")
        else:
            ago = self.git.log(
                '-2',
                '--pretty=format:last change was %cr',
                'content'
            ).stdout.decode('utf-8').splitlines()
            lines = output.splitlines()
            result = u'\n'.join(
                itertools.chain(
                    itertools.islice(
                        itertools.dropwhile(
                            lambda x: not x.startswith('@@'),
                            lines[1:],
                        ),
                        1,
                        None,
                    ),
                    itertools.islice(ago, 1, None),
                )
            )
        return result

    def default(self):
        """Return last changes in truncated unified diff format"""
        output = self.git.log(
            '-1',
            '-p',
            '--no-color',
            '--format=%s',
        ).stdout.decode('utf-8')
        lines = output.splitlines()
        return u'\n'.join(
            itertools.chain(
                lines[:1],
                itertools.islice(
                    itertools.dropwhile(
                        lambda x: not x.startswith('+++'),
                        lines[1:],
                    ),
                    1,
                    None,
                ),
            )
        )

    def verbose(self):
        """Return changes in human-friendly format #14"""
        try:
            before = self.git.show('HEAD~1:content').strip()
        except sh.ErrorReturnCode_128:
            before = None
        after = self.git.show('HEAD:content').strip()
        if before is not None:
            return (u'{subject}\nNew value:\n{after}\n'
                    u'Old value:\n{before}\n'
                    .format(subject=self.subject,
                            before=before,
                            after=after))
        else:
            return u'\n'.join([self.subject, after])

    def new(self):
        content = self.git.show('HEAD:content').strip()
        return u'\n'.join([self.subject, content])
