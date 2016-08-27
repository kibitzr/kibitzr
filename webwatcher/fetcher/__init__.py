from .browser import browser
from .simple import simple


FETCHERS = {
    'asis': simple,
    'json': simple,
    'text': browser,
    'html': browser,
}


def fetch(conf):
    return FETCHERS[conf['format']](conf)
