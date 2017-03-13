#!/usr/bin/python
# -*- coding: utf-8 -*-

from Persons import Persons


class Staff(Persons):
    def __init__(self):
        self.staffNames = []
        self.staffID = []
