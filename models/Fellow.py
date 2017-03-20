#!/usr/bin/python
# -*- coding: utf-8 -*-

from Persons import Persons


class Fellow(Persons):
    wants_space = "N"

    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name, last_name)
        self.allocated = False
