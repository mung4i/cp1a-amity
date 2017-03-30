#!/usr/bin/python
# -*- coding: utf-8 -*-


class Person(object):

    def __init__(self, first_name, last_name, role):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.employeeID = id(self)

    def __repr__(self):
        return self.first_name + ' ' + self.last_name


class Fellow(Person):
    wants_space = "N"

    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name, last_name, role='fellow')
        self.allocated = False


class Staff(Person):

    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name, role='staff')
