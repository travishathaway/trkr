#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read()

setup(
    name='citer',
    version='0.1.0',
    description='CLI tool to track time on projects',
    long_description=readme + '\n\n' + history,
    author='Travis Hathaway',
    author_email='travis.j.hathaway@gmail.com',
    url='https://github.com/travishathaway/trkr',
    packages=[
        'trkr',
        'trkr.data',
        'trkr.commands'
    ],
    entry_points={
        'console_scripts': [
            'trkr=trkr:cli'
        ]
    },
    package_dir={'trkr': 'trkr'},
    include_package_data=True,
    install_requires=[
        'requests==2.31.0',
        'Click==7.0',
        'tabulate==0.8.6',
        'xhtml2pdf==0.2.4',
        'Jinja2==2.11.3'
    ],
    license='MIT',
    zip_safe=False,
    keywords='citer',
    classifiers=[
        'License :: OSI Approved :: GNU v3',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
