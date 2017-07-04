from ampersand import build, ampersand
import sys, os, json, pystache
args = sys.argv
p = os.path # Aliasing os.path to 'p'

def call_for_help(msg):

    if msg != "":
        print(msg)

    # Command usage
    print("""
** Ampersand - the minimal translation manager **

Usage: amp <command> [args]

    new <name> [lang] - Creates an empty Ampersand website")
                serve - Compiles all modals")
     plugin <command> -  Manages plugins")
             add <name> - Adds a plugin via Git")
          remove <name> - Removes a plugin")

    """)

def amp():

    if len(args) > 1:
        if args[1] == "serve":
            # Serves all web pages
            print("Initializing the website...")
            site = ampersand.Ampersand()
            site.serve()

        elif args[1] == "new":
            if len(args) > 2:
                # Builds a new Ampersand project
                print("Creating new site '%s'" % (args[2]))
                lang = "en"
                if len(args) > 3:
                    lang = args[3]

                # Build the project tree
                print(" * Building tree")
                tree = [
                    "_modals", "_trans", p.join("_trans", lang),
                    "_layouts", "_site", "_plugins"
                ]
                try:
                    os.mkdir(args[2])
                except FileExistsError as e:
                    print(str(e))
                    sys.exit()

                for folder in tree:
                    os.mkdir(os.path.join(args[2], folder))

                # Create empty files
                abspath = p.dirname(p.abspath(__file__))
                open(p.join(args[2], "_modals/index.html"), "a+").close()
                build.build_file(p.join(abspath, "templates", "page.json"),
                                 p.join(args[2], "_trans", lang, "index.json"),
                                 {})

                # Build the _ampersand.json file
                print(" * Building _ampersand.json")
                build.build_file(
                    p.join(abspath, "templates/_ampersand.json"),
                    args[2] + "/_ampersand.json", {
                        "name": args[2],
                        "lang": lang
                    }
                )

                print("Created boilerplate website.")

            else:
                call_for_help("The command \"amp new\" takes at least two "
                            + "arguments.")

        elif args[1] == "plugin":
            if len(args) > 3:
                site = ampersand.Ampersand()

                if args[2] == "add":
                    # Add a new plugin
                    site.plugin_add(args[3])

                elif args[2] == "remove":
                    # Remove an existing plugin
                    site.plugin_remove(args[3])

            else:
                call_for_help("The command \"amp plugin\" requires at least "
                            + "three arguments")

        else:
            call_for_help("That doesn't seem to be a valid command...")

    else:
        call_for_help("Missing arguments!")
