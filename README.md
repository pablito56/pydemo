pydemo
======

Python code demonstration console for didactic purposes. Prints and executes input files in blocks.


Description
-----------

pydemo provides a command line interpreter which emulates the behavior of the interactive Python interpreter.
In addition, it can read files Python files and execute them by blocks. The CLI processes all the files and splits them in code blocks.
A certain number of empty lines in files (1 by default) are used to identify the boundaries between blocks, although they are also validated to verify that they are syntactically correct. In negative case, next lines are added until the accumulated block is right. 
Each time no text is introduced in the CLI (just pressing *ENTER* key) a new block is executed. It is print (with syntax highlighted if *Pygments* is installed) and then it is evaluated inside the CLI, so that in next command you may use objects instantiated inside the code block.


Installation
------------

Download the code and execute `python setup.py install`. After installation you will have a `pydemo` command available.


Requirements
------------

* pydemo is not compatible with Python 3.X (migration pending):
  * pydemo uses standard library's *code* and *optparse* modules. The latter is deprecated in Python 2.7 and replaced by *argparse* in Python 3.X.
  * Additional changes may be required related with encoding and how files are read. 
* To install the package you need *setuptools* or *distribute*. They are already installed from stock in several Linux flavours or in virtualenv.
* The package will try to install *Pygments* and *readline* as requirements. However, both packages are not mandatory, so you can remove them from the file `requirements.txt` and then proceed with the installation.
  * Let me remind that *readline* has some kind of incompatibilities with `pip`, so you better install it with `easy_install` beforehand.


Usage
-----
```
$ pydemo --help
Usage: pydemo [--no-history] [--no-color] [--blanks NUM] [FILES]

Frappe Context Processor Backend process

Options:
  --version     show program's version number and exit
  -h, --help    show this help message and exit
  --blanks=NUM  Number of blank lines between each code block
  --no-history  Do not use or store history
  --no-color    Do not use colorful output
```

* Use `--blanks=NUM` argument to specify minimum number of empty lines to take between each code block.
* Use `--no-history` argument to not load or store the history (you will not be able to browse it inside the CLI).
* Use `--no-color` to disable syntax highlight.

* By default pydemo will take all the `*.py` files in the folder where you launch it, in alphabetical order.
* When launched it prints a trace with information about files loaded:

```
$ pydemo
Loaded 1 files, 3 code blocks
...
```

* You may provide a list of files to read instead. You may print the list of loaded files executing command `%print_files`:

```
$ pydemo tests/test3.py
Loaded 1 files, 5 code blocks
Python 2.7.2 (default, Oct 11 2012, 20:14:37)
[GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(DemoHistoryConsole)
>>> %print_files
Loaded 1 files, 5 code blocks
In strict order:
    tests/test3.py
>>>
```

* Each time you input an empty line a new code block is executed. You may interact with that code (e.g. access instances and class and functions declarations):

```
$ pydemo tests/test3.py
Loaded 1 files, 5 code blocks
Python 2.7.2 (default, Oct 11 2012, 20:14:37)
[GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(DemoHistoryConsole)
>>>
#-*- coding: utf-8 -*-

>>>
class DemoClass(object):
    """Class to demonstrate pydemo
    """
    def __init__(self, val):
        """Constructor of the class
        """
        self.attr = val
    def power_attr(self, num):
        return num ** self.attr

>>>
inst = DemoClass(3)

>>> inst.attr
3
>>>
print inst.power_attr(2)
print inst.power_attr(3)
print inst.power_attr(4)

8
27
64
>>>
No more demo code available. Execute '%reload_files [FILENAMES]' to reload
```

* Use `%reload_files [FILENAMES]` command to reload more files (more code blocks to execute):

```
$ pydemo tests/test3.py
Loaded 1 files, 5 code blocks
Python 2.7.2 (default, Oct 11 2012, 20:14:37)
[GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(DemoHistoryConsole)
>>> %reload_files
Loaded 1 files, 5 code blocks
>>> %reload_files tests/test2.py
Loaded 1 files, 7 code blocks
>>>
```

* Use `%help` command inside CLI to check the commands:

```
$ pydemo
Loaded 1 files, 3 code blocks
Python 2.7.2 (default, Oct 11 2012, 20:14:37)
[GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(DemoHistoryConsole)
>>> %help
pydemo (DemoHistoryConsole) help:

    %reload_files [FILENAMES] => Reload files. You must provide full or relative path. The extension '.py' is optional.

    %print_files              => Print currently loaded files.

Use exit() or Ctrl-D (i.e. EOF) to exit.
```

Wishlist
--------
* Support Python 3.X
* Autocompletion
* Use a generator to load files incrementally
* Reload and reprocess files until current point (keep a "cursor")
* Use *iPython* instead of *code* module
* Implement web interface
