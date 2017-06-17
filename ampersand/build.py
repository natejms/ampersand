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
        print("It seems like you have an error in your JSON file. Check that and try again.")
        print(str(e))
        sys.exit()

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

def collect(file_name, site):
    # Create variables pointing to items in the configuration
    root = site.root
    config = site.config

    template = config["files"][file_name]
    template_path = p.join(root, "_modals", file_name)
    translation = config["files"][file_name]
    build_dir = p.join(root, config["site"])

    pages = {}

    for key, value in sorted(template.items()):
        # Read the selected file's translation into the trans variable
        try:
            trans = get_json(p.join(root, config["files"][file_name][key]))

        except OSError as e:
            print(str(e))
            sys.exit()

        # Read _global.json into _globale
        try:
            _global = get_json(p.join(root, config["translations"], key, "_global.json"))

        except OSError:
            _global = {}


        layout_files = os.listdir(p.join(root, config["layouts"]))
        layouts = {}
        for i in range(len(layout_files)):
            # Read the layout into "contents"
            contents = read_file(p.join(root, config["layouts"], layout_files[i]))
            # Render the layouts using _ampersand.json and _global.json
            layouts[p.splitext(layout_files[i])[0]] = pystache.render(
                contents, {"config": config, "global": _global})

        # Assign the collected contents to the pages dictionary
        content = {"trans": trans, "layouts": layouts, "config": config, "global": _global}

        pages[key] = content

    return pages

def build_pages(content, site):
    config = site.config
    root = site.root

    # Iterate through the plugins
    for key, value in sorted(config["plugins"].items()):
        site.plugin_run(key, content)

    # Iterate through the files
    for key, value in sorted(content.items()):
        # Iterate through the translations
        for k, v in sorted(content[key].items()):
            # Set up the tree
            if k != config["primary"]:
                if not p.exists(p.join(root, config["site"], key)):
                    os.mkdir(p.join(root, config["site"], k))

            if k != config["primary"]: build_path = p.join(k, key)
            else: build_path = key

            # Build the file
            build_file(
                p.join(root, config["modals"], key),
                p.join(site.root, site.config["site"], build_path),
                content[key][k])
