#!/usr/bin/python
# -*- coding: utf-8 -*-
from Rooms import Rooms


class Office(Rooms):
    room_capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
