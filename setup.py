#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from hfeed2atom import about

# use requirements.txt for dependencies
with open('requirements.txt') as f:
    required = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=about.NAME,
    version='.'.join(map(str, about.VERSION[0:3])) + ''.join(about.VERSION[3:]),
    description=about.SUMMARY,
    long_description=readme,
    install_requires=required,
    author=about.AUTHOR['name'],
    author_email=about.AUTHOR['contact'],
    url=about.URL['github'],
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
