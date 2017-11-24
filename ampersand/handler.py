from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from ampersand import build, ampersand
import re

def call_for_help(msg=""):

    if msg != "":
        print(msg)

    # Command usage
    print("""
** Ampersand 0.5.2 - the minimal translation manager **

Usage: amp [options] <command> [args]

                 help - Display this message
    new <name> [lang] - Creates an empty Ampersand website
                serve - Compiles all modals
     plugin <command> -  Manages plugins
               add <name> - Adds a plugin via Git
            remove <name> - Removes a plugin

         -v --verbose - Print verbose output
    """)

def amp(args, site):

    if "serve" in args:
        # Serve all of the pages
        site.serve()
    elif "plugin" in args:
        if "add" in args:
            # Add plugins
            url = re.findall(r'(https?://\S+)', " ".join(args))
            if len(url) > 1:
                for i in url:
                    site.plugin_add(i)
            elif len(url) == 1:
                site.plugin_add(url[0])
            else:
                call_for_help("The command 'amp plugin add' takes at least one "
                            + "URL.")
        elif "remove" in args:
            # Remove plugins
            removed = False
            try:
                for i in args:
                    if i in site.config["plugins"]:
                        site.plugin_remove(i)
                        removed = True

                if not removed:
                    print("Couldn't find the plugin.")

            except KeyError:
                print("No plugins installed.")
        else:
            # Call for help
            call_for_help("The command 'amp plugin' takes at least two more "
                        + "arguments.")
    else:
        # Iterate through handler plugins
        try:
            for key in sorted(site.config["plugins"].keys()):
                site.plugin_run(key, "handler", args)

        except KeyError:
            pass

        print("Nothing more to do.")
