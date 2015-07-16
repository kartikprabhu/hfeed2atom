#/usr/bin/env python

from . import about

__author__    = about.AUTHOR['name']
__contact__   = about.AUTHOR['contact']
__copyright__ = about.COPYRIGHT
__license__   = about.LICENSE
__version__   = '.'.join(map(str, about.VERSION[0:3])) + ''.join(about.VERSION[3:])

from hfeed2atom import hfeed2atom, hentry2atom
