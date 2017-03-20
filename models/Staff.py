#!/usr/bin/python
# -*- coding: utf-8 -*-

from Persons import Persons


class Staff(Persons):

    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)
