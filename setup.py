#!/usr/bin/env python

import os
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

try:
    # Might be missing if no pandoc installed
    with open('CHANGELOG.rst') as history_file:
        history = history_file.read()
except IOError:
    history = ""


def changelog_version():
    with open('CHANGELOG.md') as fp:
        for line in fp:
            if line.startswith('## '):
                version = line.split()[1].strip('[]')
                if set(version).issubset('0123456789.'):
                    return version


install_requires = [
    'bs4',
    'cachecontrol',
    'Click>=6.0',
    'entrypoints',
    'Jinja2',
    'lazy-object-proxy',
    'lxml',
    'python-telegram-bot',
    'pytimeparse',
    'pyyaml',
    'requests',
    'schedule',
    'selenium',
    'six',
]
if os.name == 'nt':
    # sh predecessor working under Windows:
    install_requires.append('pbs')
else:
    install_requires.extend(['sh', 'xvfbwrapper'])


setup(
    name='kibitzr',
    version='4.0.5',
    description="Self hosted web page changes monitoring",
    long_description=readme + '\n\n' + history,
    author="Peter Demin",
    author_email='kibitzrrr@gmail.com',
    url='https://github.com/kibitzr/kibitzr',
    packages=[
        'kibitzr',
    ],
    package_dir={
        'kibitzr': 'kibitzr',
    },
    entry_points={
        'console_scripts': [
            'kibitzr=kibitzr.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=install_requires,
    license="MIT license",
    zip_safe=False,
    keywords='kibitzr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-pep8',
        'pylint',
        'mock',
        'pytest-mock',
    ],
)
