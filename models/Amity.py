#!/usr/bin/python
# -*- coding: utf-8 -*-

from Office import Office
from LivingSpace import LivingSpace


class Amity(object):
    '''
    Rooms dictionary containing created offices or living spaces.
    Room names are stored in lists.
    '''
    rooms = {"Office": {}, "LivingSpace": {}}
    people = {
        "FELLOWS": [],
        "STAFF": []
    }

    def create_room(self, room_names_list, room_type):
        if room_type == "LivingSpace":
            for lspacename in room_names_list:
                if lspacename in self.get_roomname(list(self.rooms["LivingSpace"].keys())):
                    print "Cannot create duplicate rooms"
                    break
                else:
                    livingspace = LivingSpace(lspacename)
                    self.rooms["LivingSpace"][livingspace] = []
        if room_type == "Office":
            for ospacename in room_names_list:
                if ospacename in self.get_roomname(list(self.rooms["Office"].keys())):
                    print "Cannot create duplicate rooms"
                    break
                else:
                    office = Office(ospacename)
                    self.rooms["Office"][office] = []
                    print "Room {0} successfuly created".format(office.room_name)

    def get_roomname(self, rooms):
        all_room_names = []
        for room in rooms:
            all_room_names.append(room.room_name)
        return all_room_names

    def add_people(self, person_name, person_type, wants_space):
        pass

    def allocate_person(self):
        pass

    def return_room_allocated(self, room_name):
        pass

    def reallocatePerson(self, person_name, room_name):
        pass

    def print_rooms(self):
        pass

    def print_allocations(self, ):
        pass

    def print_unallocated(self, ):
        pass

    def save_state(self, ):
        pass

    def load_state(self, ):
        pass
