#!/usr/bin/env python

import os
from setuptools import setup

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

try:
    # Might be missing if no pandoc installed
    with open('CHANGELOG.rst', encoding='utf-8') as history_file:
        history = history_file.read()
except IOError:
    history = ""


def read_requirements():
    with open(os.path.join('requirements', 'base.in'), encoding='utf-8') as fp:
        lines = [line.split('#', 1)[0].strip()
                 for line in fp]
    # drop empty lines:
    return [line
            for line in lines
            if line and not line.startswith('#')]


install_requires = read_requirements()
if os.name == 'nt':
    # sh predecessor working under Windows:
    install_requires.append('pbs')
else:
    install_requires.extend(['sh<2'])


setup(
    name='kibitzr',
    version='7.0.2',
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
            'kibitzr=kibitzr.cli:extended_cli'
        ]
    },
    include_package_data=True,
    install_requires=install_requires,
    license="MIT license",
    zip_safe=False,
    keywords='kibitzr',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
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
