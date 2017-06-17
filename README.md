# Ampersand

The really, *really* minimalistic static site generator.

Ampersand is a minimal static site generator designed to help you manage
multiple translations of a website without needing to do so dynamically. On its
own, Ampersand is a command line utility that allows you to separate the text
content of your website from the markup and store it in a JSON file where you
can rebuild your page via Mustache templates.

Traditionally, managing translations of a website statically would look
something like this:

```
__ root
|
|__ scripts
|  |__ scripts.js
|
|__ styles
|  |__ styles.css
|
|__ lang
    |__ en
    |  |__ index.html
    |  |__ about.html
    |  |__ ...
    |
    |__ fr
        |__ index.html
        |__ about.html
        |__ ...
```

In this project, we have a website with two or more English pages that we
also translated into French. This works, but what happens when I want to make
some changes to `index.html`? In the past, it was as easy as making my changes
and saving. Now, I need to copy those changes over to the `fr` folder and
adapt.

It gets worse the more languages you add.

## How is Ampersand the solution?

Ampersand lets you create one HTML file that acts as a template and a series
of JSON files containing the translated phrases. With this, you can then compile
it into as many languages as you want.

Now, you can leave the translation to the globalization team and focus on
your code.

## Philosophy

So as you can tell, Ampersand is a pretty straightforward static site generator.
Some may even argue that it doesn't do much. This is because Ampersand is a
*minimalistic* static site generator. But of course, all static site generators
mention minimalism in their mission statement so saying it here doesn't mean
much. Never the less, Ampersand aims to do what it's supposed to do without
jumping through too many hoops that don't help it achieve its goal.

## Installation

Setting up Ampersand is fairly simple if you have `pip`. For those of you who
don't, [python.org](https://packaging.python.org/installing/) has it
documented.

```
$ pip install ampersand
```

For a bleeding edge and developer version, you can clone the repository:

```
$ git clone https://github.com/natejms/ampersand.git
$ cd ampersand
$ pip install .
```

To learn more about the usage of Ampersand, check out
[the documentation](https://github.com/natejms/ampersand/wiki)

## Contributing

Interested in making a contribution? Here's a few places where you might be
able to help out:

 * Contribute patches and help develop new features
 * Develop a plugin for Ampersand
 * Work to improve the documentation
 * Help spread the word

More information can be found in the CONTRIBUTING.md file of this repository.
