# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('chownref/chownref.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "chownref",
    packages = ["chownref"],
    entry_points = {
        "console_scripts": ['chownref = chownref.chownref:main']
        },
    version = version,
    description = "Command line application to apply ownership and group from a reference file",
    long_description = long_descr,
    author = "Amr Mostafa",
    author_email = "amr.mostafa@gmail.com",
    url = "http://github.com/amr/chownref",
    )
