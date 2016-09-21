#!/usr/bin/env python
import os
from io import open

import sh

from .utils import normalize_filename

git = sh.git.bake('--no-pager', _cwd="pages")


def report_changes(conf, content):
    return PageHistory(conf).report_changes(content)


class PageHistory(object):
    STORAGE_DIR = "pages"

    def __init__(self, conf):
        self.cwd = os.path.join(
            self.STORAGE_DIR,
            normalize_filename(conf['name']),
        )
        self.target = os.path.join(self.cwd, "content")
        self.git = sh.git.bake(
            '--no-pager',
            _cwd=self.cwd,
        )
        self.ensure_repo_exists()
        self.commit_msg = "{name} at {url}".format(
            name=conf['name'],
            url=conf.get('url'),
        )

    def report_changes(self, content):
        self.write(content)
        if self.commit():
            return True, self.last_log()
        else:
            return False, None

    def write(self, content):
        with open(self.target, 'w', encoding='utf-8') as fp:
            fp.write(content)
            if not content.endswith(u'\n'):
                fp.write(u'\n')

    def commit(self):
        self.git('add', '-A', '.')
        try:
            self.git.commit('-m', self.commit_msg)
            return True
        except sh.ErrorReturnCode_1:
            return False

    def last_log(self):
        output = self.git.log(
            '-1',
            '-p',
            '--no-color',
            '--format=%s',
        ).stdout.decode('utf-8')
        lines = output.splitlines()
        if len(lines) >= 6:
            # remove meaningless git header
            return u'\n'.join(lines[:1] + lines[6:])
        else:
            return output

    def ensure_repo_exists(self):
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)
        if not os.path.isdir(os.path.join(self.cwd, ".git")):
            self.git.init()
