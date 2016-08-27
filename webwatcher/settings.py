import yaml


with open('watch.yml') as fp:
    conf = yaml.load(fp)

PAGES = conf['pages']
