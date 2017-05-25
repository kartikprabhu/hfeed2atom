#/usr/bin/env python

from . import __about__

__author__    = __about__.AUTHOR['name']
__contact__   = __about__.AUTHOR['contact']
__copyright__ = __about__.COPYRIGHT
__license__   = __about__.LICENSE
__version__   = '.'.join(map(str, __about__.VERSION[0:3])) + ''.join(__about__.VERSION[3:])

from hfeed2atom import hfeed2atom, hentry2atom
