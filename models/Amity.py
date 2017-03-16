#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from Office import Office
from LivingSpace import LivingSpace
from Fellow import Fellow
from Staff import Staff


class Amity(object):
    '''
    Rooms dictionary containing created offices or living spaces.
    Room names are stored in lists.
    '''
    rooms = {"Office": [], "LivingSpace": []}
    people = {
        "FELLOWS": [],
        "STAFF": []
    }
    allocated = []
    unallocated_persons = []

    def create_room(self, room_names_list, room_type):
        for room in room_names_list:
            if not type(room) == str:
                print "Room name should be a string"
                break
            if room in self.get_roomname(self.rooms["LivingSpace"]):
                print "Cannot create duplicate rooms"
                break
            if room in self.get_roomname(self.rooms["Office"]):
                print "Cannot create duplicate rooms"
                break
            if room_type == "LivingSpace":
                for lspacename in room_names_list:
                    livingspace = LivingSpace(lspacename)
                    self.rooms["LivingSpace"].append(livingspace)
                    print "Room {0} successfuly created".format(
                        livingspace.room_name)
            if room_type == "Office":
                for ospacename in room_names_list:
                    office = Office(ospacename)
                    self.rooms["Office"].append(office)
                    print "Room {0} successfuly created".format(
                        office.room_name)

    def get_roomname(self, rooms):
        all_room_names = []
        for room in rooms:
            all_room_names.append(room.room_name)
        return all_room_names

    def add_people(self, person_name, person_type, wants_space):
        if person_type == "FELLOW" and wants_space == "Y":
            if type(person_name) == str:
                try:
                    fellow = Fellow(person_name)
                    print fellow.employeeID
                    self.people["FELLOWS"].append(fellow)
                    allocated = random.choice(self.get_listofrooms())
                    allocated.occupants.append(fellow)
                    self.allocated.append(fellow)
                except IndexError:
                    self.unallocated_persons.append(person_name)
                    return "Extra person not allocated added to unallocated"
        if person_type == "STAFF":
            staff = Staff(person_name)
            self.people["STAFF"].append(staff)
            if wants_space == "Y":
                print "Staff not allowed to have living spaces"

    def get_fellowobject(self, person_name):
        for person in self.people["FELLOWS"]:
            if person.name == person_name:
                return person

    def get_staffobject(self, person_name):
        for person in self.people["STAFF"]:
            if person.name == person_name:
                return person

    def get_listofrooms(self):
        all_rooms = []
        for room in self.rooms["LivingSpace"]:
            if len(room.occupants) < 4:
                all_rooms.append(room)
        # print all_rooms
        return all_rooms

    def get_livingspaceobject(self, room_name):
        for room in self.rooms["LivingSpace"]:
            if room.room_name == room_name:
                return room

    def return_people_allocated(self, person_name):
        for person in self.allocated:
            result = self.get_fellowobject(person_name)
            if result == person:
                return "{0} is allocated".format(person.name)

    def return_room_allocated(self, person_object):
        for room in self.rooms["LivingSpace"]:
            if person_object in room.occupants:
                print room.occupants
                return room
            else:
                return "Person not allocated, check in unallocated lists"

    def deallocate_fellow(self, person_object, room_object):
        if room_object in self.rooms["LivingSpace"]:
            room_object.occupants.remove(person_object)
        else:
            return "{0} not in {1}".format(
                person_object.name, room_object.room_name)

    def reallocatePerson(self, person_name, person_type, wants_space="Y"):
        if person_type == "FELLOW":
            target = self.get_fellowobject(person_name)
            assigned = self.return_room_allocated(target)
            self.deallocate_fellow(target, assigned)
            if wants_space == "Y":
                allocated = random.choice(self.get_listofrooms())
                allocated.occupants.append(target)
                print "successfuly reallocated"

    def print_rooms(self):
        room_names_list = []
        rooms = self.get_listofrooms()
        for room in rooms:
            room_names_list.append(room.room_name)
        return room_names_list

    def print_allocations(self):
        for person in self.people:
            person_obj = self.get_fellowobject(person)
            room_obj = self.return_room_allocated(person_obj)
        print (person_obj, room_obj)

    def print_unallocated(self):
        for person in self.unallocated_persons:
            print (person)

    def save_state(self, ):
        pass

    def load_state(self, ):
        pass


amity = Amity()
amity.create_room(["Java"], "LivingSpace")
print amity.get_livingspaceobject("Java")
