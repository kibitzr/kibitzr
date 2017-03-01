import copy
import logging.config

import yaml


logger = logging.getLogger(__name__)


class ReloadableSettings(object):
    _instances = {}

    def __init__(self, filename, creds_filename):
        self.filename = filename
        self.creds_filename = creds_filename
        self.pages = None
        self.notifiers = None
        self.creds = {}
        self.reread()

    @classmethod
    def instance(cls, filename, creds_filename):
        key = (filename, creds_filename)
        if key not in cls._instances:
            cls._instances[key] = cls(filename, creds_filename)
        return cls._instances[key]

    def reread(self):
        """
        Read configuration file and substitute references into pages conf
        """
        with open(self.filename) as fp:
            conf = yaml.load(fp)
        changed = self.read_creds()
        pages = conf.get('pages', [])
        notifiers = conf.get('notifiers', {})
        templates = conf.get('templates', {})
        scenarios = conf.get('scenarios', {})
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

    def read_creds(self):
        try:
            with open(self.creds_filename, 'r') as fp:
                creds = yaml.load(fp)
                if creds != self.creds:
                    self.creds = creds
                    return True
        except IOError:
            pass
        except Exception:
            logger.exception("Error loading credentials file")
        return False


def settings():
    return ReloadableSettings.instance('kibitzr.yml', 'kibitzr-creds.yml')


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
