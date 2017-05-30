from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name = "ampersand",
    version = "0.3.0",
    description = "A really, really minimalistic static site generator",
    long_description = readme(),
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Environment :: Console"
    ],
    keywords = "ampersand static site generator localization globalization translation",
    url = "http://github.com/natejms/ampersand",
    author = "Nathan Scott",
    author_email = "natejms@outlook.com",
    license = "MIT",
    packages = ["ampersand"],
    entry_points = {
        "console_scripts": ["ampersand=ampersand.command_line:main"]
    },
    install_requires = [
        "pystache"
    ],
    include_package_data = True,
    zip_safe = False
)
