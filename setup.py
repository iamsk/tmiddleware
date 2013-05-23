#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='TMiddleware',
    version='0.0.1',
    url='https://github.com/iamsk/tmiddleware',
    author='iamsk',
    author_email='iamsk.info@gmail.com',
    description='tornado middleware',
    long_description=read('README.md'),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'tornado>=2.4',
    ],
)
