#-*- coding: utf-8 -*-
u'''
TEST1: Test classes declaration with empty double lines
'''
__author__ = "Pablo Enfedaque"
__email__ = "pablito56@gmail.com"
__version__ = "0.0.1"
__license__ = "MIT"
__date__ = "Jan 23, 2013"


class MyPrintClass(object):
    class_attr = "class_attr_value"

    def __init__(self):
        self.attr = "inst_attr_value"
        self.print_count = 0

    def __str__(self):
        return " | ".join((self.class_attr, self.attr, str(self.print_count)))

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, str(self))


    def print_inst(self):
        self.print_count += 1
        print self
        print repr(self)



inst = MyPrintClass()
print inst
inst.print_inst()
