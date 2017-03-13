#!/usr/bin/python
# -*- coding: utf-8 -*-


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
        pass

    def get_roomname(self, room_name):
        pass

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
