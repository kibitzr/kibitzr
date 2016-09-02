import copy
import logging.config

import yaml


class ReloadableSettings(object):
    def __init__(self, filename):
        self.filename = filename
        self.pages = None
        self.notifiers = None
        self.reread()

    def reread(self):
        """
        Read configuration file and substitute references into pages conf
        """
        with open(self.filename) as fp:
            conf = yaml.load(fp)
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
                        if notify_param in notifiers:
                            notify[notify_type] = notifiers[notify_param]
        if self.pages != pages or self.notifiers != notifiers:
            self.pages = pages
            self.notifiers = notifiers
            return True
        else:
            return False


settings = ReloadableSettings('kibitzer.yml')


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
