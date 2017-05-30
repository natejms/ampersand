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
    try:
        return (get_json("_config.json"), p.dirname(p.abspath("./_config.json")))
    except FileNotFoundError:
        try:
            location = input("Enter the path (from here) to the root of your project: ")
            return (get_json(p.join(location, "_config.json")), p.abspath(location))
        except (KeyboardInterrupt, FileNotFoundError, NotADirectoryError) as e:
            print(str(e))
            sys.exit()

def call_for_help():
    # Command usage
    print("\n** Ampersand - the minimal translation manager **\n")
    print("Usage: ampersand <command>")
    print("   new <name> [lang] - Creates an empty Ampersand website")
    print("             compile - Compiles the specified modal")
    print("               serve - Compiles all modals\n")

def build_file(modal, new_file, content):
    # Render the template HTML file
    new_content = pystache.render(read_file(modal), content)

    # Generate the new file using the template
    generated = open(new_file, "w")
    generated.write(HTMLParser().unescape(new_content))
    generated.close()

def translate_file(file_name, config, root):
    layout_files = os.listdir(p.join(root, config["layouts"]))
    layouts = {}
    for i in range(len(layout_files)):
        contents = read_file(p.join(root, config["layouts"], layout_files[i]))
        layouts[p.splitext(layout_files[i])[0]] = contents

    # Create variables pointing to items in the configuration
    template = config["files"][file_name]
    template_path = p.join(root, "_modals", file_name)
    translation = config["files"][file_name]
    build_dir = p.join(root, config["site"])

    for key, value in sorted(template.items()):
        try:
            trans = get_json(p.join(root, config["files"][file_name][key]))
        except FileNotFoundError as e:
            print(str(e))
            sys.exit()
        if key != config["primary"]:
            if not p.exists(p.join(root, config["site"], key)):
                os.mkdir(p.join(root, config["site"], key))

        print(" * Translating '%s' in '%s'" % (template_path, key))

        # Build the translation
        if key != config["primary"]: build_path = p.join(key, file_name)
        else: build_path = file_name

        build_file(template_path,
            p.join(root, config["site"], build_path),
            {"trans": trans, "layouts": layouts, "config": config})

def ampersand():
    if len(args) > 1:
        if args[1] == "compile":
            config = open_config()
            if len(args) > 2:
                print("Compiling page '%s'" % (args[2]))
                # Iterate through the translations and insert the layouts
                try:
                    translate_file(args[2], config[0], config[1])
                except KeyError as e:
                    print("Didn't recognize %s as a file in _config.json" % args[2])
                    sys.exit()
            else:
                print("The command \"ampersand compile\" takes at least two arguments.")
                call_for_help()
        elif args[1] == "serve":
            config = open_config()
            print("Compiling all pages")
            files = config[0]["files"]
            for key, value in sorted(files.items()):
                translate_file(key, config[0], config[1])
        elif args[1] == "new":
            if len(args) > 2:
                print("Creating new site '%s'" % (args[2]))
                lang = "en"
                if len(args) > 3:
                    lang = args[3]

                print(" * Building tree")
                tree = ["_modals", "_translations", p.join("_translations", lang), "_layouts", "_site"]
                try:
                    os.mkdir(args[2])
                except FileExistsError as e:
                    print(str(e))
                    sys.exit()

                for folder in tree:
                    os.mkdir(os.path.join(args[2], folder))
                open(p.join(args[2], "_modals/index.html"), "a+").close()
                f = open(p.join(args[2], "_translations", lang, "index.json"), "a+")
                f.write("{\n\n}")
                f.close()

                print(" * Building _config.json")
                abspath = p.dirname(p.abspath(__file__))
                build_file(p.join(abspath, "templates/_config.json"), args[2] + "/_config.json", {
                    "name": args[2],
                    "lang": lang
                })
                print("Created boilerplate website.")
            else:
                print("The command \"ampersand new\" takes at least two arguments.")
                call_for_help()
        else:
            print("That doesn't seem to be a valid command...")
            call_for_help()
    else:
        call_for_help()
