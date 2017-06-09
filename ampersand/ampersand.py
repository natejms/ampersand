from ampersand import build
import sys, os
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
            build.translate_file(key, self.config, self.root)

    def compile(self, filename):
        print("Compiling page '%s'" % filename)
        # Iterate through the translations and insert the layouts
        try:
            build.translate_file(filename, self.config, self.root)
        except KeyError:
            print("Didn't recognize %s as a file in _ampersand.json" % filename)
            sys.exit()
