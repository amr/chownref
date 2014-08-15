chownref
========

Change a file's owner/group to be equal to the owner/group of another file.


Installation
============

Current master from GitHub::

    $: [sudo] pip install git+git://github.com/amr/chown-reference.git


Examples
========

Basic usage
-----------

Set the owner/group of `file2` to be the same as `file1`::

    chownref file1 file2

Do not actually do anything, just report what could have been done::

    chownref -d file1 file2

Execute and report what's done::

    chownref -v file1 file2

Execute and report what's done to standard output, and write all actions to `log.json` file (JSON format explained below)::

    chownref -v -j log.json file1 file2

This option is currently useless, it will be useful when recursive support is implemented.

Limitations
===========
The current version supports the most basic function of copying owner/group. It's currently not very useful without recursion support.


TODO:
=====
Support all options of the standard `chown`.