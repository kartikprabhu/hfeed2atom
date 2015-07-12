#/usr/bin/env python

VERSION = (0, 1, 0, "")

__author__    = 'Kartik Prabhu'
__contact__   = 'me@kartikprabhu.com'
__copyright__ = 'Copyright (c) by Kartik Prabhu'
__license__   = 'MIT'
__version__   = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])

from hfeed2atom import hfeed2atom
