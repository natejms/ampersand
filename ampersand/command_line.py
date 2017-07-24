from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from ampersand import handler, build, ampersand
import sys, os, json, pystache
args = sys.argv
p = os.path # Aliasing os.path to 'p'

def main():

    if len(args) is 1 or "help" in args:
        handler.call_for_help()
    elif "new" in args:
        build.amp_new(args)
    else:
        print("Initializing the website...")
        site = ampersand.Ampersand(("-v" in args or "--verbose" in args))
        handler.amp(args, site)
