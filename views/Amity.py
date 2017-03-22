#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from termcolor import cprint
from Room import Office, LivingSpace
from Person import Fellow, Staff


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
    office_allocations = []
    unallocated_persons = []

    def create_room(self, room_type, room_names_list):
        for room_name in room_names_list:
            if type(room_name) != str:
                self.print_error("Room name should be a string")
                return -1

            if room_name in self.get_roomname(self.rooms["LivingSpace"]):
                self.print_error("Cannot create duplicate rooms")
                return -1

            if room_name in self.get_roomname(self.rooms["Office"]):
                self.print_error("Cannot create duplicate rooms")
                return -1

            if room_type == "LivingSpace":
                livingspace = LivingSpace(room_name)
                self.rooms["LivingSpace"].append(livingspace)
                self.print_success("Living space {0} has been created".format(
                    livingspace.room_name))

            if room_type == "Office":
                office = Office(room_name)
                self.rooms["Office"].append(office)
                self.print_success("Office {0} has been created".format(
                    office.room_name))

    def add_people(self, first_name, last_name, person_type, wants_space="N"):
        if person_type == "FELLOW" and wants_space == "Y":

            if type(first_name) and type(last_name) == str:
                try:
                    allocated = random.choice(self.get_listoflspaces())
                    fellow = Fellow(first_name, last_name)
                    self.people["FELLOWS"].append(fellow)
                    self.print_success("{0} {1} added to Fellows".format(fellow.first_name,
                                                                         fellow.last_name))
                    fellow.allocated = True
                    allocated.occupants.append(fellow)
                    self.allocated_persons.append([fellow, allocated])
                    self.print_success("{0} {1} has been allocated to {2}".format(
                        fellow.first_name, fellow.last_name,
                        allocated.room_name))

                except IndexError:
                    fellow = Fellow(first_name, last_name)
                    self.people["FELLOWS"].append(fellow)
                    self.unallocated_persons.append(fellow)
                    self.print_error("No rooms to add people to.\n\
                    Please create a room \n\
                    Extra person not allocated added to unallocated")

        if person_type == "STAFF" and wants_space == "N":
            staff = Staff(first_name, last_name)
            self.people["STAFF"].append(staff)

        elif person_type == "STAFF" and wants_space == "Y":
            self.print_error("Staff not allowed to have living spaces")

    def allocate_person(self, first_name, last_name, person_type, room_type):
        person_obj = self.get_fellowobject(first_name, last_name)
        if room_type == "Office":
            try:
                random_rooms = random.choice(self.get_listofoffices())

                if person_obj in self.unallocated_persons:
                    self.office_allocations.append([person_obj, random_rooms])
                    random_rooms.occupants.append(person_obj)
                    self.people["FELLOWS"].append(person_obj)
                    self.print_success("{0} {1} was allocated to {2}".format(
                        person_obj.first_name, person_obj.last_name,
                        random_rooms.room_name))

                else:
                    self.print_error("{0} {1} is already allocated.\n\
                    Please try reallocating".format(
                        first_name, last_name))
            except IndexError:
                self.print_error("You need to create rooms")

    def deallocate_fellow(self, person_object, room_object):
        if room_object in self.rooms["LivingSpace"]:
            room_object.occupants.remove(person_object)
            search = [person_object, room_object]
            for search in self.allocated_persons:
                self.allocated_persons.remove(search)
        else:
            self.print_error("{0} {1} not in this room ".format(
                person_object.first_name,
                person_object.last_name))

    def reallocate_person(self, first_name, last_name, person_type, room_name):
        target = self.get_fellowobject(first_name, last_name)
        assigned = self.return_room_allocated(target)
        if target:
            if person_type == "FELLOW":
                self.deallocate_fellow(target, assigned)
                new_room = self.get_roomobject(room_name)
                new_room.occupants.append(target)
                self.allocated_persons.append([target, new_room])
                self.print_success("{0} {1} was reallocated to {2}".format(
                    target.first_name, target.last_name, new_room.room_name))
        else:
            self.print_error("{0} {1} does not exist".format(first_name,
                                                             last_name))

    def print_rooms(self):
        room_names_list = []
        rooms = self.get_listoflspaces()
        o_rooms = self.get_listofoffices()
        for room in rooms:
            room_names_list.append(room.room_name)
        for room in o_rooms:
            room_names_list.append(room.room_name)
        for room in room_names_list:
            self.print_success(room)

    def print_allocations(self):
        if len(self.allocated_persons) > 0:
            for person in self.allocated_persons:
                try:
                    self.print_success("{0} {1} was allocated to {2}".format(
                        person[0].first_name, person[0].last_name,
                        person[1].room_name))
                except AttributeError:
                    self.print_error(
                        "Add a room so {0} {1} can be allocated".format(
                            person[0].first_name, person[0].last_name))
        else:
            self.print_error(
                "Fellows have not been allocated yet, Please add a fellow")

    def print_unallocated(self):
        open("unallocated.txt", "w").close()
        for person in self.unallocated_persons:
            self.print_success("{0} {1}".format(
                person.first_name, person.last_name))
            with open("unallocated.txt", "a") as myfile:
                myfile.write(person.first_name + " " + person.last_name +
                             "FELLOW" + " " + "Y" + '\n')
                myfile.close()

    def print_room_members(self, room_name):
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
                self.print_success("{0} has the following members".format(
                    room_name))
                for memberz in member:
                    self.print_success("{0}".format(memberz.name))
            else:
                self.print_error("empty")

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
                self.add_people(first_name, last_name, person_type,
                                wants_space="N")
        self.print_success("People loaded successfully")

    def get_roomname(self, rooms):
        all_room_names = []
        for room in rooms:
            all_room_names.append(room.room_name)
        return all_room_names

    def get_fellowobject(self, first_name, last_name):
        for person in self.people["FELLOWS"]:
            if person.first_name == first_name and \
                    person.last_name == last_name:
                return person

    def get_roomobject(self, room_name):
        for room in self.rooms["LivingSpace"]:
            if room.room_name == room_name:
                return room

    def get_officeobject(self, room_name):
        for room in self.rooms["Office"]:
            if room.room_name == room_name:
                return room

    def get_staffobject(self, first_name, last_name):
        for person in self.people["STAFF"]:
            if person.first_name == first_name and \
                    person.last_name == last_name:
                return person

    def get_listofoffices(self):
        all_rooms = []
        for rooms in self.rooms["Office"]:
            if len(rooms.occupants) < 6:
                all_rooms.append(rooms)
        return all_rooms

    def get_listoflspaces(self):
        all_rooms = []
        for room in self.rooms["LivingSpace"]:
            if len(room.occupants) < 4:
                all_rooms.append(room)
        return all_rooms

    def return_people_allocated(self):
        for person in self.people["FELLOWS"]:
            if person.allocated is True:
                return person

    def return_room_allocated(self, person_object):
        for room in self.rooms["LivingSpace"]:
            if person_object in room.occupants:
                return room
            else:
                return "Person not allocated, check in unallocated lists"

    def print_success(self, text):

        cprint(text, 'green')

    def print_error(self, text):
        cprint(text, 'red')

    def print_info(self, text):
        cprint(text, 'yellow')
