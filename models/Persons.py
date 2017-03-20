#!/usr/bin/python
# -*- coding: utf-8 -*-


class Persons(object):

    def __init__(self, name):
        self.name = name
        self.employeeID = id(self)
