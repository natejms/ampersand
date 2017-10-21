from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from setuptools import setup

def readme():
    with open("README.rst", encoding="utf8") as f:
        return f.read()

setup(
    name = "ampersand",
    version = "0.5.1",
    description = "The really, really minimalistic static site generator",
    long_description = readme(),
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Environment :: Console"
    ],
    keywords = "ampersand amp static site generator localization globalization translation",
    url = "http://github.com/natejms/ampersand",
    author = "Nathan Scott",
    author_email = "natejms@outlook.com",
    license = "MIT",
    packages = ["ampersand"],
    entry_points = {
        "console_scripts": [
            "ampersand=ampersand.command_line:main",
            "amp=ampersand.command_line:main"
        ]
    },
    install_requires = [
        "pystache",
        "future"
    ],
    include_package_data = True,
    zip_safe = False
)
