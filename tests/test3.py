#-*- coding: utf-8 -*-


class DemoClass(object):
    """Class to demonstrate pydemo
    """
    def __init__(self, val):
        """Constructor of the class
        """
        self.attr = val

    def power_attr(self, num):
        return num ** self.attr


inst = DemoClass(3)

print inst.power_attr(2)
print inst.power_attr(3)
print inst.power_attr(4)
