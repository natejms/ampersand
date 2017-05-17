import sys
import os
import json
import pystache
from html.parser import HTMLParser
from subprocess import call

args = sys.argv

def open_config():
    # Read the config file into a variable
    try:
        f = open("_config.json", "r")
        config = json.loads(f.read())
        f.close()
        return config
    except json.decoder.JSONDecodeError as e:
        print("It seems like you have an error in your _config.json file.\n" +
            "Check that and try again.")
        print(str(e))
        sys.exit()

def call_for_help():
    # Command usage
    print("\n** Ampersand - the minimal translation manager **\n")
    print("Usage: ampersand <command>")
    print("        new <name> - Creates an empty Ampersand website")
    print("           compile - Compiles the specified modal")
    print("             serve - Compiles all modals\n")

def is_ampersand():
    if os.path.isfile("_config.json"):
        return True
    else:
        print("This folder doesn't seem to be a valid Ampersand site.\nTry " +
            "running this command again from the root of the project.")
        return False

def build_file(modal, new_file, content):

    # Render the template HTML file
    origin = open(modal, "r")
    template = origin.read()
    new_content = pystache.render(template, content)
    origin.close()

    # Generate the new file using the template
    generated = open(new_file, "w")
    generated.write(HTMLParser().unescape(new_content))
    generated.close()

def translate_file(file_name, config):

    layout_files = os.listdir("_layouts")
    layouts = {}
    for i in range(len(layout_files)):
        f = open(os.path.join(config["layouts"], layout_files[i]), "r")
        contents = f.read()
        f.close()

        layouts[os.path.splitext(layout_files[i])[0]] = contents

    # Create variables pointing to items in the configuration
    template = config["files"][file_name]
    template_path = "_modals/" + file_name
    translation = config["files"][file_name]
    build_dir = config["site"] + "/"

    for key, value in sorted(template.items()):
        modal = open(config["files"][file_name][key], "r")
        try:
            trans = json.loads(modal.read())
        except json.decoder.JSONDecodeError as e:
            print("It seems like you have a problem with one of your " +
                "translation files. Check that and then try again.")
            print(str(e))
            sys.exit()
        modal.close()

        if not os.path.exists(config["site"]+"/"+key):
            call(["mkdir", config["site"]+"/"+key])
        print(" * Translating '%s' in '%s'" % (template_path, key))

        # Build the translation
        build_file(template_path,
            os.path.join(config["site"], key, file_name),
            {"trans": trans, "layouts": layouts, "config": config})

def ampersand():
    if len(args) > 1:
        if args[1] == "compile" and is_ampersand():
            config = open_config()
            if len(args) > 2:
                print("Compiling page '%s'" % (args[2]))

                # Iterate through the translations and insert the layouts
                translate_file(args[2], config)

        elif args[1] == "serve"  and is_ampersand():
            config = open_config()

            print("Compiling all pages")
            files = config["files"]
            for key, value in sorted(files.items()):
                translate_file(key, config)

        elif args[1] == "new":
            if len(args) > 2:

                print("Creating new site '%s'" % (args[2]))

                path = os.path.abspath(args[2])
                lang = "en"
                if len(args) > 3:
                    lang = args[3]

                print(" * Building tree")
                call(["mkdir", args[2]])
                call(["mkdir", os.path.join(args[2], "_modals")])
                open(os.path.join(args[2], "_modals/index.html"), "a+").close()
                call(["mkdir", os.path.join(args[2], "_translations")])
                call(["mkdir", os.path.join(args[2], "_translations", lang)])
                f = open(os.path.join(args[2], "_translations", lang, "index.json"), "a+")
                f.write("{\n\n}")
                f.close()
                call(["mkdir", os.path.join(args[2], "_layouts")])
                call(["mkdir", os.path.join(args[2], "_site")])

                print(" * Building _config.json")
                abspath = os.path.dirname(os.path.abspath(__file__))
                build_file(os.path.join(abspath, "templates/_config.json"), args[2] + "/_config.json", {
                    "name": args[2],
                    "lang": lang,
                    "path": path
                })
                print("Created boilerplate website.")
            else:
                call_for_help()
        else:
            call_for_help()
    else:
        call_for_help()
