import os
import re
import copy
import logging.config
import contextlib

import yaml


logger = logging.getLogger(__name__)


class ConfigurationError(RuntimeError):
    pass


class ReloadableSettings(object):
    _instance = None
    CONFIG_DIRS = (
        '',
        '~/.config/kibitzr/',
        '~/',
    )
    CONFIG_FILENAME = 'kibitzr.yml'
    CREDENTIALS_FILENAME = 'kibitzr-creds.yml'
    RE_PUNCTUATION = re.compile(r'\W+')
    UNNAMED_PATTERN = 'Unnamed check {0}'

    def __init__(self, config_dir):
        self.filename = os.path.join(config_dir, self.CONFIG_FILENAME)
        self.creds_filename = os.path.join(config_dir,
                                           self.CREDENTIALS_FILENAME)
        self.pages = None
        self.notifiers = None
        self.creds = {}
        self.reread()

    @classmethod
    def detect_config_dir(cls):
        candidates = [
            (directory, os.path.join(directory, cls.CONFIG_FILENAME))
            for directory in map(os.path.expanduser, cls.CONFIG_DIRS)
        ]
        for directory, file_path in candidates:
            if os.path.exists(file_path):
                return directory
        raise ConfigurationError(
            "kibitzr.yml not found in following locations: %s"
            % ", ".join([x[1] for x in candidates])
        )

    @classmethod
    def instance(cls):
        if cls._instance is None:
            config_dir = cls.detect_config_dir()
            cls._instance = cls(config_dir)
        return cls._instance

    def reread(self):
        """
        Read configuration file and substitute references into pages conf
        """
        logger.debug("Loading settings from %s",
                     os.path.abspath(self.filename))
        conf = self.read_conf()
        changed = self.read_creds()
        pages = conf.get('checks', conf.get('pages', []))
        notifiers = conf.get('notifiers', {})
        templates = conf.get('templates', {})
        scenarios = conf.get('scenarios', {})
        unnamed_check_counter = 1
        pages = list(self.unpack_batches(pages))
        for i, page in enumerate(pages):
            if not page.get('name'):
                if page.get('url'):
                    page['name'] = self.url_to_name(page['url'])
                else:
                    page['name'] = self.UNNAMED_PATTERN.format(unnamed_check_counter)
                    unnamed_check_counter += 1
            name = page['name']
            if 'template' in page:
                if page['template'] in templates:
                    templated_page = copy.deepcopy(templates[page['template']])
                else:
                    raise ConfigurationError(
                        "Template %r not found. Referenced in page %r"
                        % (page['template'], name)
                    )
                templated_page.update(page)
                page = templated_page
                del page['template']
                pages[i] = page
            if 'scenario' in page:
                if page['scenario'] in scenarios:
                    page['scenario'] = scenarios[page['scenario']]
            if 'notify' in page:
                for notify in page['notify']:
                    if hasattr(notify, 'keys'):
                        notify_type = next(iter(notify.keys()))
                        notify_param = next(iter(notify.values()))
                        try:
                            notify[notify_type] = notifiers[notify_param]
                        except (TypeError, KeyError):
                            # notify_param is not a predefined notifier name
                            # Save it as is:
                            notify[notify_type] = notify_param
        if self.pages != pages or self.notifiers != notifiers:
            self.pages = pages
            self.notifiers = notifiers
            return True
        else:
            return changed

    @classmethod
    def url_to_name(cls, url):
        return cls.RE_PUNCTUATION.sub('-', url)

    def unpack_batches(self, pages):
        for page in pages:
            if 'batch' in page:
                base = copy.deepcopy(page)
                batch = base.pop('batch')
                url_pattern = base.pop('url-pattern')
                items = base.pop('items')
                for item in items:
                    new_page = copy.deepcopy(base)
                    new_page['name'] = batch.format(item)
                    new_page['url'] = url_pattern.format(item)
                    yield new_page
            else:
                yield page

    def read_conf(self):
        """
        Read and parse configuration file
        """
        with self.open_conf() as fp:
            return yaml.load(fp)

    @contextlib.contextmanager
    def open_conf(self):
        with open(self.filename) as fp:
            yield fp

    def read_creds(self):
        """
        Read and parse credentials file.
        If something goes wrong, log exception and continue.
        """
        logger.debug("Loading credentials from %s",
                     os.path.abspath(self.creds_filename))
        creds = {}
        try:
            with self.open_creds() as fp:
                creds = yaml.load(fp)
        except IOError:
            logger.info("No credentials file found at %s",
                        os.path.abspath(self.creds_filename))
        except:
            logger.exception("Error loading credentials file")
        if creds != self.creds:
            self.creds = creds
            return True
        return False

    @contextlib.contextmanager
    def open_creds(self):
        with open(self.creds_filename) as fp:
            yield fp


def settings():
    """
    Returns singleton instance of settings
    """
    return ReloadableSettings.instance()


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'sh': {
            'level': 'INFO',
        },
        'sh.command': {
            'level': 'WARNING',
        },
    }
})
