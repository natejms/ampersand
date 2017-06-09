from ampersand import build, ampersand
import sys, os, json, pystache
args = sys.argv
p = os.path # Aliasing os.path to 'p'

def call_for_help():
    # Command usage
    print("\n** Ampersand - the minimal translation manager **\n")
    print("Usage: amp <command>")
    print("   new <name> [lang] - Creates an empty Ampersand website")
    print("             compile - Compiles the specified modal")
    print("               serve - Compiles all modals\n")

def amp():
    if len(args) > 1:
        if args[1] == "compile":
            site = ampersand.Ampersand()
            if len(args) > 2:
                site.compile(args[2])
            else:
                print("The command \"amp compile\" takes at least three arguments.")
                call_for_help()
        elif args[1] == "serve":
            site = ampersand.Ampersand()
            site.serve()
        elif args[1] == "new":
            if len(args) > 2:
                print("Creating new site '%s'" % (args[2]))
                lang = "en"
                if len(args) > 3:
                    lang = args[3]

                print(" * Building tree")
                tree = ["_modals", "_trans", p.join("_trans", lang), "_layouts", "_site"]
                try:
                    os.mkdir(args[2])
                except FileExistsError as e:
                    print(str(e))
                    sys.exit()

                for folder in tree:
                    os.mkdir(os.path.join(args[2], folder))
                open(p.join(args[2], "_modals/index.html"), "a+").close()
                f = open(p.join(args[2], "_trans", lang, "index.json"), "a+")
                f.write("{\n\n}")
                f.close()

                print(" * Building _ampersand.json")
                abspath = p.dirname(p.abspath(__file__))
                build.build_file(p.join(abspath, "templates/_ampersand.json"), args[2] + "/_ampersand.json", {
                    "name": args[2],
                    "lang": lang
                })
                print("Created boilerplate website.")
            else:
                print("The command \"amp new\" takes at least two arguments.")
                call_for_help()
        else:
            print("That doesn't seem to be a valid command...")
            call_for_help()
    else:
        call_for_help()
