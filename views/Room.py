#!/usr/bin/python
# -*- coding: utf-8 -*-


class Room(object):
    room_capacity = None

    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name
        self.occupants = []

    def __repr__(self):
        return self.room_name


class LivingSpace(Room):
    room_capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)


class Office(Room):
    room_capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
