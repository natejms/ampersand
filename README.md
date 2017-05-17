# Ampersand
A really, *really* minimalistic static site generator.

Ampersand is the product of being annoyed by how difficult it is to maintain
a web application's translations by copying and pasting the source code into
language denoted folders, Apache Cordova not having any native method of
managing translations and an afternoon to kill.

## What is Ampersand?

Ampersand is a lightweight and minimalistic static site generator with the
primary focus of managing translations of a user interface via the Moustache
template engine and a whole bunch of JSON.

Traditionally, managing translations of a website would look something like
this:

```
__ root
|
|__ scripts
____|__ scripts.js
|
|__ styles
____|__ styles.css
|
|__ lang
    |__ en
        |__ index.html
        |__ about.html
     ___|__ ...
    |
    |__ fr
        |__ index.html
        |__ about.html
        |__ ...

```

In this project, we have a website with two or more English pages that were
also translated into French. This works, but what happens when I want to make
some changes to `index.html`? In the past, it was as easy as making my changes
and saving. Now, I need to copy those changes over to the `fr` folder and
adapt.

It gets worse the more languages you add.

## How is Ampersand the solution?

Ampersand lets you create one HTML file that acts as a template and a series
of JSON files containing the translated phrases. With this, you can then compile
it into as many languages as you want.

With it, you can leave the translation to the localization team and focus on
your code.

## Using Ampersand

First of all, you'll need to set it up.

```
$ pip install ampersand
```

Then, you can create a new Ampersand site like so:

```
$ ampersand new MyWebsite en
```

The `ampersand new` command takes two arguments: your title and primary
language. The title is required, though the primary language can be ommited,
defaulting to English (en)

You don't *need* to refer to each language with its two letter code, but it
works well from an organizational standpoint.

Next, develop your webpage using Moustache templates in the place of each frase.
Once finished, create a JSON file with the same name to contain your
translations. For an example,

`_modals/index.html`
```
<!DOCTYPE html>
<html>
  <body>
    <h1>{{ trans.header }}</h1>
    <p>{{ trans.tagline }}</p>
  </body>
</html>
```

`_translations/en/index.json`
```
{
  "header": "A new Ampersand website",
  "tagline": "The really, <em>really</em> minimalistic static site generator"
}
```

Once you have your pages set up, run the following command to compile your pages
into the `_site` directory.

```
$ ampersand serve
```

## Configuration

Every Ampersand site comes with a file named `_config.json` (incase you were
wondering, this `_config.json` file is how Ampersand recognizes a directory
as an Ampersand site). This file comes with some basic configurations that you
can change at any time. By default, it should look something like this:

```
{
  "name": "Ampersand",
  "primary": "en",
  "path": "/home/you/Documents/Ampersand",
  "layouts": "_layouts",
  "modals": "_modals",
  "translations": "_translations",
  "site": "_site",
  "files": {
    "index.html": {
      "en": "_translations/en/index.json",
    }
  }
}

```

Every new translation should be added to the object associated with the file
in `_config.json`.

## Other commands

### Compiling files individually

Usage: ampersand compile <filename>

Example:
```
$ ampersand compile _moduals/index.html
```
