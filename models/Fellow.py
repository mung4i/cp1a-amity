#!/usr/bin/python
# -*- coding: utf-8 -*-

from Persons import Persons


class Fellow(Persons):
    wants_space = "N"

    def __init__(self, name):
        super(Fellow, self).__init__(name)
        self.allocated = False
