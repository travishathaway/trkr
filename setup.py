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
    ],
    entry_points={
        'console_scripts': [
            'trkr=trkr:cli'
        ]
    },
    package_dir={'trkr': 'trkr'},
    include_package_data=True,
    install_requires=[
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
