from ampersand import build
from shutil import rmtree
import sys, os, json, subprocess, importlib, inspect
p = os.path

class Ampersand(object):
    """docstring for Ampersand."""
    def __init__(self):

        try:
            config = build.get_json("_ampersand.json")
            root = p.dirname(p.abspath("./_ampersand.json"))
        except FileNotFoundError:
            try:
                location = input("Enter the path (from here) to the root of your project: ")
                config = build.get_json(p.join(location, "_ampersand.json"))
                root = p.abspath(location)
            except (KeyboardInterrupt, FileNotFoundError, NotADirectoryError) as e:
                print(str(e))
                sys.exit()

        self.root = root
        self.config = config


    def serve(self):
        print("Compiling all pages")
        for key, value in sorted(self.config["files"].items()):
            build.translate_file(key, self)

    def compile(self, filename):
        print("Compiling page '%s'" % filename)
        # Iterate through the translations and insert the layouts
        try:
            build.translate_file(filename, self)
        except KeyError:
            print("Didn't recognize %s as a file in _ampersand.json" % filename)
            sys.exit()

    def plugin_add(self, url):
        try:
            plugin = p.splitext(p.split(url)[1])[0]
            plugin_path = p.join(self.root, self.config["modules"], plugin)
            print("Installing Ampersand plugin '%s'" % plugin)

            subprocess.call(["git", "clone", url, plugin_path])

            self.config["plugins"][p.basename(plugin)] = p.join(self.config["modules"], plugin)
            updated = open(p.join(self.root, "_ampersand.json"), "w")
            updated.write(json.dumps(self.config, indent=4))
            updated.close()
        except KeyError as e:
            print("Missing entry in your configuration file: %s" % str(e))

    def plugin_remove(self, name):
        try:
            print("Removing plugin '%s'" % name)
            rmtree(p.join(self.root, self.config["plugins"][name]))

            self.config["plugins"].pop(name)
            updated = open(p.join(self.root, "_ampersand.json"), "w")
            updated.write(json.dumps(self.config, indent=4))
            updated.close()
        except KeyError:
            print("Failed to remove plugin '%s' as it is not installed." % name)
            sys.exit()

    def plugin_run(self, name, content):
        try:
            plugin = build.get_json(p.join(self.root, self.config["plugins"][name], "_plugin.json"))
            sys.path.append(p.join(self.root, self.config["plugins"][name]))
            print(p.join(self.root, self.config["plugins"][name]))
            module = importlib.import_module("main", name)
            content = module.main(content)
            return content
        except (KeyError, FileNotFoundError) as e:
            print("Failed to run plugin '%s': %s" % (name, e))
            return content
