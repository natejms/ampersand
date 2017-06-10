import sys, os, json, pystache
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

def build_file(modal, new_file, content):
    # Render the template HTML file
    new_content = pystache.render(read_file(modal), content)

    # Generate the new file using the template
    generated = open(new_file, "w")
    generated.write(new_content)
    generated.close()

def translate_file(file_name, site):
    # Create variables pointing to items in the configuration
    root = site.root
    config = site.config

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

        try:
            _global = get_json(p.join(root, config["translations"], key, "_global.json"))
        except FileNotFoundError:
            _global = {}

        layout_files = os.listdir(p.join(root, config["layouts"]))
        layouts = {}
        for i in range(len(layout_files)):
            contents = read_file(p.join(root, config["layouts"], layout_files[i]))
            layouts[p.splitext(layout_files[i])[0]] = pystache.render(
                contents, {"config": config, "global": _global})

        for t_key, t_value in sorted(trans.items()):
            if t_value.startswith("file:"):
                trans[t_key] = read_file(
                    p.join(root, p.dirname(translation[key]),
                    t_value.replace("file:", "")))

        if key != config["primary"]:
            if not p.exists(p.join(root, config["site"], key)):
                os.mkdir(p.join(root, config["site"], key))

        print(" * Translating '%s' in '%s'" % (template_path, key))

        # Build the translation
        if key != config["primary"]: build_path = p.join(key, file_name)
        else: build_path = file_name

        content = {"trans": trans, "layouts": layouts, "config": config, "global": _global}
        for key, value in sorted(site.config["plugins"].items()):
            content = site.plugin_run(key, content)

        build_file(template_path,
            p.join(root, config["site"], build_path), content)
