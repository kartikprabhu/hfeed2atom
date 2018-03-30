#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os.path

_ABOUT_ = {}
_PATH_ = os.path.dirname(__file__)

with open(os.path.join(_PATH_, 'hfeed2atom/__about__.py'))\
        as about_file:
    exec(about_file.read(), _ABOUT_)

# use requirements.txt for dependencies
with open(os.path.join(_PATH_, 'requirements.txt')) as f:
    required = map(lambda s: s.strip(), f.readlines())

with open(os.path.join(_PATH_, 'README.md')) as f:
    readme = f.read()

with open(os.path.join(_PATH_, 'LICENSE')) as f:
    license = f.read()

setup(
    name = _ABOUT_['NAME'],
    version = '.'.join(map(str, _ABOUT_['VERSION'][0:3])) + ''.join(_ABOUT_['VERSION'][3:]),
    description = _ABOUT_['SUMMARY'],
    long_description = readme,
    install_requires = required,
    dependency_links=[
        "https://github.com/kartikprabhu/mf2py/tarball/experimental#egg=mf2py-1.1.1"
    ],
    author = _ABOUT_['AUTHOR']['name'],
    author_email = _ABOUT_['AUTHOR']['email'],
    url = _ABOUT_['URL']['github'],
    license = license,
    packages = find_packages(exclude=('tests', 'docs'))
)
