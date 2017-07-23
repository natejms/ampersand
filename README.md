# Ampersand

The really, *really* minimalistic static site generator. Manage translations
statically, without any pesky JavaScript for rendering dynamic chunks of
localized text.

## Features
 * Separate key phrases (or everything, for that matter) into "modals" and
 localized content files.
 * Create includes such as site-wide headers and footers to reduce repetition.
 * Avoid copy and pasting the same content several times with global
 translations.
 * Keep things simple with Mustache templates.
 * Extend Ampersand with plugins written in Python.

## The problem
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

Here, we have a website with two or more English pages that we also translated
into French. This works, but what happens when I want to make some changes to
`index.html`? Now, I need to copy those changes over to the `fr` folder and
adapt. When these phrases are wrapped with new UI components, It gets worse the
more languages you add.

## The solution

A problem like this would take a static site generator to solve, but not just
any static site generator would do the trick. This generator must have a
focus on translation, allowing you to build several copies of the same page
based on different localization files.

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
