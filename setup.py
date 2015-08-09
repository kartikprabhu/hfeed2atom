#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# use requirements.txt for dependencies
with open('requirements.txt') as f:
    required = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hfeed2atom',
    version='0.2.1',
    description='Converter from h-feed microformats to Atom 1.0',
    long_description=readme,
    install_requires=required,
    author='Kartik Prabhu',
    author_email='me@kartikprabhu.com',
    url='https://github.com/kartikprabhu/hfeed2atom',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
