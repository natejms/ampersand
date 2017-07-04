import sys, os, json, pystache
p = os.path # Aliasing os.path to 'p'

def read_file(path):

    # Open a file and return its contents
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def get_json(path):

    # Load a JSON file into a dictionary
    try:
        return json.loads(read_file(path))

    except json.decoder.JSONDecodeError as e:
        print("It seems like you have an error in your JSON file. Check that "
            + "and try again.")
        print(str(e))
        sys.exit()

def get_content(path):

    page = read_file(path)
    page = page.split("}}}", 1)

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

def collect(site):

    # Create variables pointing to items in the configuration
    root = site.root
    config = site.config

    content = {}

    lang = [name for name in
           os.listdir(p.join(root, config["translations"]))
           if p.isdir(p.join(root, config["translations"], name))]

    for directory in lang:
        lang_dir = p.join(root, config["translations"], directory)
        pages = os.listdir(lang_dir)
        content[directory] = {}

        for page in pages:
            if not p.isdir(page):

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
        site.plugin_run(key, content)

    for lang in sorted(content.keys()):
        if lang != config["primary"]:
            if not p.exists(p.join(root, config["site"], config["primary"])):
                os.mkdir(p.join(root, config["site"], config["primary"]))

        for page in sorted(content[lang].keys()):

            if content[lang][page]["frontmatter"] == {}:
                print(" ** Skipping '%s': Error in the front matter" % page)
                continue

            fm = content[lang][page]["frontmatter"]
            try:
                build_file(p.join(root, config["modals"], fm["modal"]),
                           p.join(root, config["site"], fm["url"]),
                           content[lang][page])

            except OSError as e:
                print(" ** Skipping '%s': %s" % (page, str(e)))
