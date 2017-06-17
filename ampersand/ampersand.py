from ampersand import build
from shutil import rmtree
import sys, os, json, subprocess, importlib, inspect
p = os.path

class Ampersand(object):

    """docstring for Ampersand."""

    def __init__(self):

        # Attempt to find the _ampersand.json configuration file
        try:
            config = build.get_json("_ampersand.json")
            root = p.dirname(p.abspath("./_ampersand.json"))

        except OSError:
            # Ask the user where to find the _ampersand.json file

            try:
                location = input("Enter the path (from here) to the root of "
                                + "your project: ")
                config = build.get_json(p.join(location, "_ampersand.json"))
                root = p.abspath(location)

            except (KeyboardInterrupt, OSError) as e:

                print(str(e))
                sys.exit()

        self.root = root
        self.config = config

    def serve(self):

        print(" * Collecting all pages")

        # Create an empty dictionary to store each pages content
        pages = {}
        for key, value in sorted(self.config["files"].items()):
            # Iterate through the files to build the pages dictionary
            pages[key] = build.collect(key, self)

        # Build the pages
        print(" * Building pages")
        build.build_pages(pages, self)

        print("Done.")

    def compile(self, filename):

        # Try to build the specified page
        print("Compiling page '%s'" % filename)
        try:
            print(" * Building page")
            build.build_pages({filename: build.collect(filename, self)}, self)

        except KeyError:
            # Exit if not found in _ampersand.json
            print("Didn't recognize %s as a file in _ampersand.json" % filename)
            sys.exit()

        print("Done.")

    def plugin_add(self, url):

        try:
            # Decide on what to call the plugin and its path
            plugin = p.splitext(p.split(url)[1])[0]
            plugin_path = p.join(self.root, self.config["modules"], plugin)

            # Download the plugin via git
            print("Installing Ampersand plugin '%s'" % plugin)
            try:
                clone = subprocess.check_call(["git", "clone", url, plugin_path])

                # Update the _ampersand.json file by adding the plugin
                self.config["plugins"][p.basename(plugin)] = p.join(
                    self.config["modules"], plugin )
                updated = open(p.join(self.root, "_ampersand.json"), "w")
                updated.write(json.dumps(self.config, indent=4))
                updated.close()
            except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
                print(str(e))
                sys.exit()

        except KeyError as e:
            print("Missing entry in your configuration file: %s" % str(e))

    def plugin_remove(self, name):

        try:
            # Delete the directory containing the plugin
            print("Removing plugin '%s'" % name)
            rmtree(p.join( self.root, self.config["modules"], name ))
        except FileNotFoundError:
            pass

        try:
            # Update _ampersand.json by adding the plugin
            self.config["plugins"].pop(name)
            updated = open(p.join(self.root, "_ampersand.json"), "w")
            updated.write(json.dumps(self.config, indent=4))
            updated.close()
        except KeyError:
            print("Failed to remove plugin '%s' as it is not installed." % name)
            sys.exit()

    def plugin_run(self, name, content):

        try:
            # Retrieve the _plugin.json file
            plugin = build.get_json(
                p.join(self.root, self.config["plugins"][name], "_plugin.json"))

            # Load and run the module
            sys.path.append(p.join(self.root, self.config["plugins"][name]))
            module = importlib.import_module(plugin["init"], name)
            content = module.main(content, self)
            return content

        except (KeyError, FileNotFoundError,
                ImportError, AttributeError) as e:
            print("Failed to run plugin '%s': %s" % (name, e))
            return content
