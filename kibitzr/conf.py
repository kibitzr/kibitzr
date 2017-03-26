import os
import copy
import logging.config

import yaml


logger = logging.getLogger(__name__)


class ReloadableSettings(object):
    _instances = {}
    CONFIG_DIRS = (
        '',
        '~/.config/kibitzr/',
        '~/',
    )
    CONFIG_FILENAME = 'kibitzr.yml'
    CREDENTIALS_FILENAME = 'kibitzr-creds.yml'

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
        for directory in map(os.path.expanduser, cls.CONFIG_DIRS):
            if os.path.exists(os.path.join(directory, cls.CONFIG_FILENAME)):
                return directory

    @classmethod
    def instance(cls, config_dir):
        key = config_dir
        if key not in cls._instances:
            cls._instances[key] = cls(key)
        return cls._instances[key]

    def reread(self):
        """
        Read configuration file and substitute references into pages conf
        """
        logger.debug("Loading settings from %s",
                     os.path.abspath(self.filename))
        with open(self.filename) as fp:
            conf = yaml.load(fp)
        changed = self.read_creds()
        pages = conf.get('checks', conf.get('pages', []))
        notifiers = conf.get('notifiers', {})
        templates = conf.get('templates', {})
        scenarios = conf.get('scenarios', {})
        pages = list(self.unpack_batches(pages))
        for i, page in enumerate(pages):
            name = page['name']
            if 'template' in page:
                if page['template'] in templates:
                    templated_page = copy.deepcopy(templates[page['template']])
                else:
                    raise RuntimeError(
                        "Template %r not found. Referenced in page %r"
                        % (page['template'], name)
                    )
                templated_page.update(page)
                page = templated_page
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

    def read_creds(self):
        """
        Read and parse credentials file.
        If something goes wrong, log exception and continue.
        """
        logger.debug("Loading credentials from %s",
                     os.path.abspath(self.creds_filename))
        try:
            with open(self.creds_filename, 'r') as fp:
                creds = yaml.load(fp)
                if creds != self.creds:
                    self.creds = creds
                    return True
        except IOError:
            logger.info("No credentials file found at %s",
                        os.path.abspath(self.creds_filename))
        except:
            logger.exception("Error loading credentials file")
        return False


def settings():
    """
    Returns singleton instance of settings
    """
    config_dir = ReloadableSettings.detect_config_dir()
    return ReloadableSettings.instance(config_dir)


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
