from ampersand import build, ampersand
import re

def call_for_help(msg=""):

    if msg != "":
        print(msg)

    # Command usage
    print("""
** Ampersand - the minimal translation manager **

Usage: amp <command> [args]

                 help - Display this message
    new <name> [lang] - Creates an empty Ampersand website
                serve - Compiles all modals
     plugin <command> -  Manages plugins
               add <name> - Adds a plugin via Git
            remove <name> - Removes a plugin
    """)

def amp(args, site):

    if "serve" in args:
        site.serve()
    elif "plugin" in args:
        if "add" in args:
            url = re.findall(r'(https?://\S+)', " ".join(args))
            if len(url) > 1:
                for i in url:
                    site.plugin_add(i)
            else:
                site.plugin_add(url[0])
        elif "remove" in args:
            removed = False
            for i in args:
                if i in site.config["plugins"]:
                    site.plugin_remove(i)
                    removed = True

            if not removed:
                print("Couldn't find the plugin.")
        else:
            call_for_help("The command 'amp plugin' takes at least two more "
                        + "arguments.")
    else:
        call_for_help("That doesn't seem to be a valid command.")
