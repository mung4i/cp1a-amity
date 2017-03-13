#!/usr/bin/python
# -*- coding: utf-8 -*-

from Persons import Persons


class Staff(Persons):

    def __init__(self, name):
        super(Staff, self).__init__(name)


sm = Staff("Martin")
print sm.name
