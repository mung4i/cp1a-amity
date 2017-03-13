#!/usr/bin/python
# -*- coding: utf-8 -*-


class Rooms:
    room_capacity = None

    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name
