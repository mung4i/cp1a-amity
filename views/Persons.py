#!/usr/bin/python
# -*- coding: utf-8 -*-


class Persons(object):

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.employeeID = id(self)


class Fellow(Persons):
    wants_space = "N"

    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name, last_name)
        self.allocated = False


class Staff(Persons):

    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)
