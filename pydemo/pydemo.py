#! /usr/bin/env python
#-*- coding: utf-8 -*-
u"""
Created on Nov 13, 2012

@author: pablito56

@license: MIT

@contact: pablito56@gmail.com

Pydemo main module
"""


__author__ = "Pablo Enfedaque"
__email__ = "pablito56@gmail.com"
__version__ = "0.0.4"
__license__ = "MIT"
__date__ = "2012-11-13"
__updated__ = "2013-04-21"


# Std lib imports
from sys import argv, path as syspath
from os import path, listdir
import code
import atexit
from optparse import OptionParser


FORMATTER_STYLE = 'emacs'
#===============================================================================
# TO GET ALL THE AVAILABLE PIGMENTS STYLES:
# python -c "from pygments.styles import get_all_styles; print list(get_all_styles())"
#===============================================================================
RELOAD_FILES_CMD = 'reload_files'
PRINT_FILES_CMD = 'print_files'
HELP_CMD = "help"
BLANKS = 1


class HistoryConsole(code.InteractiveConsole, object):
    '''Add history support to code.InteractiveConsole like done in
    http://docs.python.org/2/library/readline.html?highlight=readline#example
    '''
    def __init__(self, histfile=path.expanduser("~/.pydemo_history"), *args, **kargs):
        super(HistoryConsole, self).__init__(*args, **kargs)
        self.init_history(histfile)

    def init_history(self, histfile):
        import readline
#        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        import readline
        readline.write_history_file(histfile)


class DemoConsole(code.InteractiveConsole, object):
    def __init__(self, files=None, blanks=BLANKS, color=True, *args, **kargs):
        self.color = color
        if not files:
            self.files = sorted([f for f in listdir(".") if f.endswith(".py") and path.isfile(f)])
        else:
            self.files = files
        self.blanks = blanks
        self.reload_files()
        syspath.append(path.abspath("."))
        super(DemoConsole, self).__init__(*args, **kargs)

    def clean_block_trail(self, block):
        '''Remove last empty as well as last break line of given code block
        '''
        while True:
            if not block[-1].strip():
                block.pop(-1)
            else:
                break
        block[-1] = block[-1].replace("\n", "")
        return block

    def get_code_blocks(self):
        '''Retrieve a list of code blocks; lists of strings containing lines of code
        :param files: list of files to read
        :return list of lists of single line strings
        '''
        blocks = []
        files_count = 0
        for index, fil in enumerate(self.files):
            if not path.isfile(fil):
                self.files = self.files[:index]
                break
            files_count += 1
            with open(fil) as f:
                curr_block = []
                found_blanks = 0
                for line in f:
                    if not line.strip():
                        found_blanks += 1
                        if curr_block and found_blanks == self.blanks:
                            blocks.append(self.clean_block_trail(curr_block))
                            curr_block = []
                            found_blanks = 0
                        elif curr_block:
                            curr_block.append(line)
                    else:
                        found_blanks = 0
                        curr_block.append(line)
                if curr_block:
                    blocks.append(self.clean_block_trail(curr_block))
                    curr_block = []
        return blocks

    def reload_files(self, new_files=None):
        if new_files:
            x = ""
            new_files = map(lambda x: x if x.endswith(".py") else x + ".py", new_files)
            filtered_new_files = filter(path.isfile, new_files)
            self.files = filtered_new_files if filtered_new_files else self.files
        self.code_block = []
        self.is_executable = False
        self.blocks = self.get_code_blocks()
        self.blocks_iter = iter(self.blocks)
        self.print_loaded_resume()

    def print_loaded_resume(self):
        self.write("Loaded {0} files, {1} code blocks\n".format(len(self.files), len(self.blocks)))

    def push(self, line):
        if not line.strip() and len(self.buffer) == 0:
            # Accumulate next code blocks until they are executable (and execute them)
            while True:
                try:
                    b = self.blocks_iter.next()
                except StopIteration:
                    if self.code_block:
                        b = []
                        self.is_executable = True
                        is_compilable = True
                    else:
                        msg = "No more demo code available. Execute '%{0} [FILENAMES]' to reload\n"
                        self.write(msg.format(RELOAD_FILES_CMD))
                        return False
                else:
                    try:
                        is_compilable = code.compile_command("".join(b), "<stdin>", "exec") is not None
                    except SyntaxError:
                        is_compilable = False
                if self.is_executable and is_compilable:
                    code_to_print = "".join(self.code_block)
                    if self.color:
                        try:
                            # Pygments imports
                            from pygments import highlight
                            from pygments.lexers import PythonLexer
                            from pygments.formatters import Terminal256Formatter
                            code_to_print = highlight("".join(self.code_block),
                                                      PythonLexer(),
                                                      Terminal256Formatter(style=FORMATTER_STYLE))
                        except ImportError:
                            pass
                    print code_to_print
                    map(super(DemoConsole, self).push,
                        [line[:-1] if line[-1] == "\n" else line for line in self.code_block if line != '\n'])
                    super(DemoConsole, self).push("\n")
                    self.code_block = b
                    self.is_executable = True
                    return False
                if self.code_block:
                    self.code_block.extend(['\n'] * self.blanks)
                self.code_block.extend(b)
                try:
                    self.is_executable = code.compile_command("".join(self.code_block), "<stdin>", "exec") is not None
                except Exception, e:
                    import traceback
                    print "EXCEPTION WHILE TRYING TO COMPILE:"
                    print "".join(self.code_block)
                    print traceback.format_exc()
            return False
        elif line.strip().startswith('%' + RELOAD_FILES_CMD) and len(self.buffer) == 0:
            self.reload_files(line.strip().split(" ")[1:])
            return False
        elif line.strip().startswith('%' + PRINT_FILES_CMD) and len(self.buffer) == 0:
            self.print_loaded_resume()
            msg = "In strict order:\n    {0}\n".format("\n    ".join(self.files))
            self.write(msg)
            return False
        elif line.strip().startswith('%' + HELP_CMD) and len(self.buffer) == 0:
            self.write(self.get_help())
            return False
        return super(DemoConsole, self).push(line)

    def get_help(self):
        '''Return a string with a help message
        '''
        help_txt = "pydemo ({}) help:\n\n".format(self.__class__.__name__)
        help_txt += "    %{:<24} => Reload files. You must provide full or relative path. \
The extension '.py' is optional.\n\n".format(RELOAD_FILES_CMD + " [FILENAMES]")
        help_txt += "    %{:<24} => Print currently loaded files.\n\n".format(PRINT_FILES_CMD)
        help_txt += "Use exit() or Ctrl-D (i.e. EOF) to exit.\n\n".format(PRINT_FILES_CMD)
        return help_txt


class DemoHistoryConsole(HistoryConsole, DemoConsole):
    pass


def demo_console(files, blanks, hist, color):
    '''Launch the demo console infinite input loop
    '''
    console = None
    if hist:
        try:
            import readline
            console = DemoHistoryConsole(files=files, blanks=blanks, color=color)
        except ImportError:
            pass
    if console is None:
        console = DemoConsole(files=files, blanks=blanks, color=color)
    console.interact()


def parse_args(in_argv=argv):
    '''pydemo command line arguments parsing function
    :param in_argv: incoming argv tuple to be parsed
    :return tuple with all decoded arguments
    '''
    usage = '''USAGE: %prog [--no-history] [--no-color] [--blanks NUM] [FILES]'''

    desc = '''Frappe Context Processor Backend process'''

    parser = OptionParser(usage=usage, version="%prog v0.0.1",
                          description=desc, prog='pydemo')

    parser.add_option('--blanks', dest='blanks', metavar='NUM',
                      help='Number of blank lines between each code block',
                      type='int', default=BLANKS)

    parser.add_option('--no-history', dest='hist',
                      help='Do not use or store history',
                      action="store_false", default=True)
    parser.add_option('--no-color', dest='color',
                      help='Do not use colorful output',
                      action="store_false", default=True)

    (opts, args) = parser.parse_args(in_argv)
    return opts.blanks, opts.hist, opts.color, args[1:]


def main():
    blanks, hist, color, files = parse_args(argv)
    demo_console(files, blanks, hist, color)


if __name__ == '__main__':
    main()
