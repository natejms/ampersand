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
        site = ampersand.Ampersand()
        handler.amp(args, site)
