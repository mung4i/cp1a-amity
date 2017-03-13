#!/usr/bin/python
# -*- coding: utf-8 -*-

from Rooms import Rooms


class LivingSpace(Rooms):
    room_capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)


ls = LivingSpace("Python")
print ls.room_name
