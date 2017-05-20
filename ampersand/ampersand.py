import sys
import os
import json
import pystache
from html.parser import HTMLParser

args = sys.argv
p = os.path # Aliasing os.path to 'p'

def read_file(path):
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def get_json(path):
    try:
        return json.loads(read_file(path))
    except json.decoder.JSONDecodeError as e:
        print("It seems like you have an error in your JSON file.\n" +
            "Check that and try again.")
        print(str(e))
        sys.exit()

def open_config():
    # Read the config file into a variable
    try:
        return get_json("_config.json")
    except FileNotFoundError:
        try:
            return get_json(input("Enter the path (from here) to your _config.json file: "))
        except KeyboardInterrupt as e:
            print(str(e))
            sys.exit()
def call_for_help():
    # Command usage
    print("\n** Ampersand - the minimal translation manager **\n")
    print("Usage: ampersand <command>")
    print("   new <name> [lang] - Creates an empty Ampersand website")
    print("             compile - Compiles the specified modal")
    print("               serve - Compiles all modals\n")

def is_ampersand(config):
    if config["path"] in p.abspath("./"):
        return True
    else:
        print("This folder doesn't seem to be a valid Ampersand site.\nTry " +
            "running this command again from the root of the project.")
        return False

def build_file(modal, new_file, content):
    # Render the template HTML file
    new_content = pystache.render(read_file(modal), content)

    # Generate the new file using the template
    generated = open(new_file, "w")
    generated.write(HTMLParser().unescape(new_content))
    generated.close()

def translate_file(file_name, config):
    layout_files = os.listdir(p.join(config["path"], config["layouts"]))
    layouts = {}
    for i in range(len(layout_files)):
        contents = read_file(p.join(config["path"], config["layouts"], layout_files[i]))
        layouts[p.splitext(layout_files[i])[0]] = contents

    # Create variables pointing to items in the configuration
    template = config["files"][file_name]
    template_path = p.join(config["path"], "_modals", file_name)
    translation = config["files"][file_name]
    build_dir = p.join(config["path"], config["site"])

    for key, value in sorted(template.items()):
        trans = get_json(p.join(config["path"], config["files"][file_name][key]))

        if key != config["primary"]:
            if not p.exists(p.join(config["path"], config["site"], key)):
                os.mkdir(p.join(config["path"], config["site"], key))

        print(" * Translating '%s' in '%s'" % (template_path, key))

        # Build the translation
        if key != config["primary"]: build_path = p.join(key, file_name)
        else: build_path = file_name

        build_file(template_path,
            p.join(config["path"], config["site"], build_path),
            {"trans": trans, "layouts": layouts, "config": config})

def ampersand():
    if len(args) > 1:
        if args[1] != "new":
            config = open_config()
            if args[1] == "compile":

                print("Compiling page '%s'" % (args[2]))

                # Iterate through the translations and insert the layouts
                try:
                    translate_file(args[2], config)
                except KeyError as e:
                    print("Didn't recognize %s as a file in _config.json" % args[2])
                    sys.exit()
            elif args[1] == "serve":

                print("Compiling all pages")
                files = config["files"]
                for key, value in sorted(files.items()):
                    translate_file(key, config)
        else:
            if len(args) > 2:
                print("Creating new site '%s'" % (args[2]))

                path = p.abspath(args[2])
                lang = "en"
                if len(args) > 3:
                    lang = args[3]

                print(" * Building tree")
                os.mkdir(args[2])
                os.mkdir(p.join(args[2], "_modals"))
                open(p.join(args[2], "_modals/index.html"), "a+").close()
                os.mkdir(p.join(args[2], "_translations"))
                os.mkdir(p.join(args[2], "_translations", lang))
                f = open(p.join(args[2], "_translations", lang, "index.json"), "a+")
                f.write("{\n\n}")
                f.close()
                os.mkdir(p.join(args[2], "_layouts"))
                os.mkdir(p.join(args[2], "_site"))

                print(" * Building _config.json")
                abspath = p.dirname(p.abspath(__file__))
                build_file(p.join(abspath, "templates/_config.json"), args[2] + "/_config.json", {
                    "name": args[2],
                    "lang": lang,
                    "path": path
                })
                print("Created boilerplate website.")
            else:
                print("The command \"ampersand new\" takes at least two arguments.")
                call_for_help()
    else:
        call_for_help()
