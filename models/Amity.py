#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
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
    allocated_persons = []
    unallocated_persons = []

    def create_room(self, room_name, room_type):
        if type(room_name) != str:
            print "Room name should be a string"
            try:
                sys.exit()
            except:
                print "Exception accomodates tdd"
        if room_name in self.get_roomname(self.rooms["LivingSpace"]):
            print "Cannot create duplicate rooms"
            try:
                sys.exit()
            except:
                print "Exception accomodates tdd"
        if room_name in self.get_roomname(self.rooms["Office"]):
            print "Cannot create duplicate rooms"
            try:
                sys.exit()
            except:
                print "Exception accomodates tdd"
        if room_type == "LivingSpace":
            livingspace = LivingSpace(room_name)
            self.rooms["LivingSpace"].append(livingspace)
            print "Living space {0} successfuly created".format(
                livingspace.room_name)
        if room_type == "Office":
            office = Office(room_name)
            self.rooms["Office"].append(office)
            print "Room {0} successfuly created".format(
                office.room_name)

    def add_people(self, first_name, last_name, person_type, wants_space="N"):
        if person_type == "FELLOW" and wants_space == "Y":
            if type(first_name) and type(last_name) == str:
                try:
                    if len(self.get_listofrooms()) != 0:
                        fellow = Fellow(first_name, last_name)
                        self.people["FELLOWS"].append(fellow)
                        allocated = random.choice(self.get_listofrooms())
                        fellow.allocated = True
                        allocated.occupants.append(fellow)
                        self.allocated_persons.append([fellow, allocated])
                    else:
                        fellow = Fellow(first_name, last_name)
                        self.unallocated_persons.append(fellow)
                        return "No rooms to add people to please create a room"
                except IndexError:
                    fellow = Fellow(first_name, last_name)
                    self.unallocated_persons.append(fellow)
                    return "Extra person not allocated added to unallocated"
        if person_type == "STAFF" and wants_space == "N":
            staff = Staff(first_name, last_name)
            self.people["STAFF"].append(staff)
        elif person_type == "STAFF" and wants_space == "Y":
            print "Staff not allowed to have living spaces"

    def allocate_person(self, first_name, last_name, person_type, room_name):
        person_obj = self.get_fellowobject(first_name, last_name)
        if person_obj not in self.unallocated_persons:
            room = self.get_roomobject(room_name)
            room.occupants.append(person_obj)
            self.allocated_persons.persons([person_obj, room])
            print "{0} was reallocated to {1}".format(
                person_obj.first_name, person_obj.last_name, room.room_name)

        else:
            print "{0} is already allocated, try reallocating.\
                Call help for assistance".format(first_name, last_name)

    def deallocate_fellow(self, person_object, room_object):
        if room_object in self.rooms["LivingSpace"]:
            room_object.occupants.remove(person_object)
            self.allocated_persons.remove([person_object, room_object])
        else:
            return "{0} not in a room".format(person_object, room_object)

    def reallocatePerson(self, first_name, last_name, person_type, room_name):
        target = self.get_fellowobject(first_name, last_name)
        assigned = self.return_room_allocated(target)
        if target not in self.people["FELLOWS"]:
            print "{0} does not exit".format(first_name, last_name)
            try:
                sys.exit()
            except:
                print "Exception accomodates tdd"
        if person_type == "FELLOW":
            self.deallocate_fellow(target, assigned)
            new_room = self.get_roomobject(room_name)
            new_room.occupants.append(target)
            self.allocated_persons.append([target, new_room])
            print "{0} was reallocated to {1}".format(
                target.name, new_room.room_name)

    def get_roomname(self, rooms):
        all_room_names = []
        for room in rooms:
            all_room_names.append(room.room_name)
        return all_room_names

    def get_fellowobject(self, first_name, last_name):
        for person in self.people["FELLOWS"]:
            if person.first_name == first_name and person.last_name == last_name:
                return person

    def get_roomobject(self, room_name):
        for room in self.rooms["LivingSpace"]:
            if room.room_name == room_name:
                return room

    def get_staffobject(self, first_name, last_name):
        for person in self.people["STAFF"]:
            if person.first_name == first_name and person.last_name == last_name:
                return person

    def get_listofrooms(self):
        all_rooms = []
        for room in self.rooms["LivingSpace"]:
            if len(room.occupants) < 4:
                all_rooms.append(room)
        for rooms in self.rooms["Office"]:
            if len(room.occupants) < 4:
                all_rooms.append(rooms)
        return all_rooms

    def get_livingspaceobject(self, room_name):
        for room in self.rooms["LivingSpace"]:
            if room.room_name == room_name:
                return room

    def return_people_allocated(self):
        for person in self.people["FELLOWS"]:
            if person.allocated is True:
                return person

    def return_room_allocated(self, person_object):
        for room in self.rooms["LivingSpace"]:
            if person_object in room.occupants:
                print room.occupants
                return room
            else:
                return "Person not allocated, check in unallocated lists"

    def print_rooms(self):
        room_names_list = []
        rooms = self.get_listofrooms()
        for room in rooms:
            room_names_list.append(room.room_name)
        return room_names_list

    def print_allocations(self):
        if len(self.allocated_persons) > 0:
            for person in self.allocated_persons:
                try:
                    print "{0} was allocated to {1}".format(
                        person[0].first_name, person[0].last_name, person[1].room_name)
                except AttributeError:
                    print "END OF LIST"
        else:
            print "Fellows have not been allocated yet, Please add a fellow"

    def print_unallocated(self):
        open("unallocated.txt", "w").close()
        for person in self.unallocated_persons:
            print (person.first_name, person.last_name)
            with open("unallocated.txt", "a") as myfile:
                myfile.write(person.first_name + " " + person.last_name +
                             "FELLOW" + " " + "Y" + '\n')
                myfile.close()

    def print_room(self, room_name):
        members = []
        obj = self.get_roomobject(room_name)
        if obj in self.rooms["LivingSpace"]:
            member = obj.occupants
            members.append(member)
        elif obj in self.rooms["Office"]:
            memberz = obj.occupants
            members.append(memberz)
        for member in members:
            if member:
                print "{0} has the following members".format(room_name)
                for memberz in member:
                    print "{0}".format(memberz.name)
            else:
                print "empty"

    def load_people(self):
        r = open("txtfile.txt", "r")
        next = r.read().splitlines()
        for word in next:
            word = word.split(" ")
            words = list(word)
            first_name = words[0]
            last_name = words[1]
            person_type = words[2]
            if len(words) == 4:
                self.add_people(first_name, last_name, person_type, words[3])
            elif len(words) <= 3:
                self.add_people(first_name, last_name, person_type, wants_space="N")
        return "People loaded successfully"
