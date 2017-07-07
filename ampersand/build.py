import sys, os, json, pystache
p = os.path # Aliasing os.path to 'p'

def read_file(path):

    # Open a file and return its contents
    try:
        with open(path, "r") as f:
            return f.read()
    except PermissionError as e:
        print(str(e))
        sys.exit()

def get_json(path):

    # Load a JSON file into a dictionary
    try:
        return json.loads(read_file(path))

    except json.decoder.JSONDecodeError as e:
        print("Failed to get JSON from '%s': %s" % (path, str(e)))
        sys.exit()

def get_content(path):

    # Collect front matter and content
    page = read_file(path)
    page = page.split("}}}", 1)

    # Load front matter into a dictionary
    try:
        content = page[1]
        try:
            frontmatter = json.loads("{ %s }" % page[0])
        except json.decoder.JSONDecodeError:
            frontmatter = {}
    except IndexError:
        content = page[0]
        frontmatter = {}

    return (frontmatter, content)

def build_file(modal, new_file, content):

    # Render the template HTML file
    new_content = pystache.render(read_file(modal), content)

    # Generate the new file using the template
    try:
        generated = open(new_file, "w")
    except FileNotFoundError:
        os.makedirs(p.dirname(new_file))
        generated = open(new_file, "w")

    generated.write(new_content)
    generated.close()

def amp_new(args):
    # Builds a new Ampersand project

    if args[2][0] is not "-":
        i = 2
        name = args[i]
    else:
        i = 3
        name = args[i]

    lang = "en"
    if len(args) > i + 1:
        lang = args[i + 1]

    print("Creating new site '%s'" % (name))

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
        os.mkdir(os.path.join(name, folder))

    # Create empty files
    abspath = p.dirname(p.abspath(__file__))
    open(p.join(name, "_modals", "index.html"), "a+").close()
    build_file(p.join(abspath, "templates", "page.json"),
                     p.join(args[2], "_trans", lang, "index.json"),
                     {})

    # Build the _ampersand.json file
    print(" * Building _ampersand.json")
    build_file(
        p.join(abspath, "templates", "_ampersand.json"),
        p.join(args[2], "_ampersand.json"), {
            "name": name,
            "lang": lang
        })

    print("Created boilerplate website.")

def collect(site):
    # Create variables pointing to items in the configuration
    root = site.root
    config = site.config

    content = {}

    # Collect the translation's files into a list
    lang = [name for name in
           os.listdir(p.join(root, config["translations"]))
           if p.isdir(p.join(root, config["translations"], name))]

    for directory in lang:
        # Looping through the language directories
        lang_dir = p.join(root, config["translations"], directory)
        pages = []

        # Iterate through directories and subdirectories
        for path, dirs, files in os.walk(p.join(config["translations"], )):
            # Iterate through each file
            for f in files:
                # Skip '_trans/lang' when taking the path
                f_list = os.path.normpath(p.join(path, f)).split(p.sep)
                pages.append(p.join(*f_list[2:]))

        content[directory] = {}

        for page in pages:
            # Looping through the pages
            if not p.isdir(page):
                # Getting the front matter
                try:
                    trans = json.loads(read_file(p.join(lang_dir, page)))
                    page_content = {}
                    try:
                        frontmatter = trans["_frontmatter"]
                    except KeyError:
                        frontmatter = {}
                except json.decoder.JSONDecodeError:
                    trans = {}
                    text = get_content(p.join(lang_dir, page))
                    frontmatter = text[0]
                    page_content = text[1]

                # Getting the global translations
                try:
                    _global = get_json(p.join(lang_dir, "_global.json"))
                except OSError:
                    _global = {}

                layout_files = os.listdir(p.join(root, config["layouts"]))
                layouts = {}

                for i in range(len(layout_files)):
                    # Read the layout into "contents"
                    contents = read_file(p.join(root,
                                                config["layouts"],
                                                layout_files[i]))

                    # Render the layouts using _ampersand.json and _global.json
                    layouts[p.splitext(layout_files[i])[0]] = pystache.render(
                        contents, {"config": config, "global": _global})

                content[directory][page] = {
                    "frontmatter": frontmatter, "trans": trans,
                    "content": page_content, "layouts": layouts,
                    "config": config, "global": _global
                }

    return content

def build_pages(content, site):

    config = site.config
    root = site.root

    # Iterate through the plugins
    for key, value in sorted(config["plugins"].items()):
        site.plugin_run(key, "builder", content)

    for lang in sorted(content.keys()):
        # Loop through each language dictionary
        if lang != config["primary"]:
            if not p.exists(p.join(root, config["site"], config["primary"])):
                os.mkdir(p.join(root, config["site"], config["primary"]))

        for page in sorted(content[lang].keys()):
            # Loop through each page
            if content[lang][page]["frontmatter"] == {}:
                print(" ** Skipping '%s': Error in the front matter" % page)
                continue

            # Build the pages
            fm = content[lang][page]["frontmatter"]
            try:
                build_file(p.join(root, config["modals"], fm["modal"]),
                           p.join(root, config["site"], fm["url"]),
                           content[lang][page])

            except OSError as e:
                print(" ** Skipping '%s': %s" % (page, str(e)))
