import yaml


with open('watch.yml') as fp:
    conf = yaml.load(fp)

PAGES = conf.get('pages', [])
NOTIFIERS = conf.get('notifiers', {})
