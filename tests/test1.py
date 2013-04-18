#-*- coding: utf-8 -*-
u'''
TEST1: Test classes declaration with empty lines
'''


__author__ = "Pablo Enfedaque"
__email__ = "pablito56@gmail.com"
__version__ = "0.0.3"
__license__ = "MIT"
__date__ = "Jan 23, 2013"


class MyClass(object):
    class_attr = "class_attr_value"

    def __init__(self):
        self.attr = "inst_attr_value"

    def __str__(self):
        return " | ".join((self.class_attr, self.attr))



inst = MyClass()
print inst
