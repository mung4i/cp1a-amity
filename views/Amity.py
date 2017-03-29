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
    unallocated_persons = []

    def create_room(self, room_type, room_names_list):
        for room_name in room_names_list:
            if not room_name.isalpha():
                self.print_error("\nRoom name should be a string")
                return -1

            if room_name in self.get_roomname(self.rooms["LivingSpace"]):
                self.print_error("\nCannot create duplicate rooms")
                return -1

            if room_name in self.get_roomname(self.rooms["Office"]):
                self.print_error("\nCannot create duplicate rooms")
                return -1

            if room_type == "LivingSpace":
                livingspace = LivingSpace(room_name)
                self.rooms["LivingSpace"].append(livingspace)
                self.print_success("\nLiving space {0} has been"
                                   " created".format(
                                       livingspace.room_name))

            if room_type == "Office":
                office = Office(room_name)
                self.rooms["Office"].append(office)
                self.print_success("\nOffice {0} has been created".format(
                    office.room_name))

    def add_person_fellow(self, first_name, last_name, person_type,
                          wants_space="N"):
        if type(first_name) and type(last_name) is str:
            try:
                if person_type == "FELLOW" and wants_space == "Y":
                    allocated_room = random.choice(self.get_listoflspaces())
                    fellow = Fellow(first_name, last_name)
                    if not self.check_if_fellow_exists(fellow):
                        return
                    self.people["FELLOWS"].append(fellow)
                    fellow.allocated = True
                    allocated_room.occupants.append(fellow)
                    self.print_success(
                        "\n{0} {1} has been allocated to {2}".format(
                            fellow.first_name,
                            fellow.last_name,
                            allocated_room.room_name))
                    self.allocate_person(first_name, last_name, "FELLOW",
                                         "Office")
            except IndexError:
                fellow = Fellow(first_name, last_name)
                if not self.check_if_fellow_exists(fellow):
                    return
                self.people["FELLOWS"].append(fellow)
                self.unallocated_persons.append(fellow)
                self.print_error("\nNo rooms to add {0} to.\n Please"
                                 " create a room.\n Extra person not "
                                 "allocated added to waiting list".format(
                                     first_name))

            if person_type == "FELLOW" and wants_space == "N":
                try:
                    fellow = Fellow(first_name, last_name)
                    if not self.check_if_fellow_exists(fellow):
                        return
                    self.people["FELLOWS"].append(fellow)
                    fellow.allocated = False
                    self.allocate_person(first_name, last_name, "FELLOW",
                                         "Office")
                except IndexError:
                    fellow = Fellow(first_name, last_name)
                    if not self.check_if_fellow_exists(fellow):
                        return
                    self.people["FELLOWS"].append(fellow)
                    self.unallocated_persons.append(fellow)
                    self.print_error("\nNo rooms to add Fellow to.\n Please"
                                     " create a room.\n Extra person not "
                                     "allocated added to waiting list")

    def add_person_staff(self, first_name, last_name, person_type,
                         wants_space="N"):
        if type(first_name) and type(last_name) is str:
            if person_type == "STAFF" and wants_space == "N":
                staff = Staff(first_name, last_name)
                if not self.check_if_staff_exists(staff):
                    return
                self.people["STAFF"].append(staff)
                self.allocate_person(first_name, last_name, "STAFF",
                                     "Office")

            if person_type == "STAFF" and wants_space == "Y":
                self.print_error("Staff not allowed to have living spaces")
                new_staff = Staff(first_name, last_name)
                if not self.check_if_staff_exists(new_staff):
                    return
                self.people["STAFF"].append(new_staff)
                self.allocate_person(first_name, last_name, "STAFF",
                                     "Office")

    def check_if_fellow_exists(self, new_fellow):
        if new_fellow.employeeID in [fellow.employeeID
                                     for fellow in self.people["FELLOWS"]]:
            self.print_error("\nCannot create fellow with the same name")
            return -1
        else:
            self.print_success("\n{0} {1} added to Fellows".format(
                new_fellow.first_name, new_fellow.last_name))
            return True

    def check_if_staff_exists(self, new_staff):
        if new_staff.employeeID in [staff.employeeID
                                    for staff in self.people["STAFF"]]:
            self.print_error("\nCannot create staff member with \
            the same name")
            return -1
        else:
            self.print_success("\n{0} {1} added to Staff".format(
                new_staff.first_name, new_staff.last_name))
            return True

    def allocate_person(self, first_name, last_name, person_type, room_type):
        try:
            if room_type == "Office":

                random_room = random.choice(self.get_listofoffices())
                if person_type == "FELLOW":
                    person_obj = self.get_fellowobject(first_name, last_name)
                    random_room.occupants.append(person_obj)
                    self.print_success("\n{0} {1} was"
                                       " allocated to {2}\n".format(
                                           person_obj.first_name,
                                           person_obj.last_name,
                                           random_room.room_name))
                    return 1
                elif person_type == "STAFF":
                    person_obj = self.get_staffobject(first_name, last_name)
                    random_room.occupants.append(person_obj)
                    self.print_success("\n{0} {1} was"
                                       "allocated to {2}\n".format(
                                           person_obj.first_name,
                                           person_obj.last_name,
                                           random_room.room_name))
                    return 1

                else:
                    self.print_error("\n {0} {1} is already allocated.\n\
                    Please try reallocating".format(
                        first_name, last_name))
                    return -1
            if room_type == "LivingSpace":
                allocated_room = random.choice(self.get_listoflspaces())
                fellow = self.get_fellowobject(first_name, last_name)
                allocated_room.occupants.append(fellow)
                self.print_success(
                    "\n{0} {1} has been allocated to {2}".format(
                        fellow.first_name,
                        fellow.last_name,
                        allocated_room.room_name))
                self.unallocated_persons.remove(person_obj)
                return 1

        except IndexError:
            self.print_error("You need to create rooms")
            person_obj = self.get_staffobject(first_name, last_name)
            self.unallocated_persons.append(person_obj)

    def deallocate_fellow(self, person_object, room_object):
        if room_object in self.rooms["LivingSpace"]:
            room_object.occupants.remove(person_object)
        else:
            self.print_error("\n{0} {1} not in this room ".format(
                person_object.first_name,
                person_object.last_name))

    def reallocate_person(self, first_name, last_name, person_type, room_name):
        target = self.get_fellowobject(first_name, last_name)
        assigned = self.return_room_allocated(target)
        try:
            if target:
                if person_type == "FELLOW":
                    self.deallocate_fellow(target, assigned)
                    new_room = self.get_roomobject(room_name)
                    new_room.occupants.append(target)
                    self.print_success("\n{0} {1} was reallocated to"
                                       "{2}".format(
                                           target.first_name, target.last_name,
                                           new_room.room_name))
            else:
                self.print_error("\n{0} {1} does not exist".format(first_name,
                                                                   last_name))
        except AttributeError:
            self.print_error("\nAllocate {0} {1}\
                             to Livingspace instead of office")

    def print_room(self, room_name):
        for room in self.rooms["Office"]:
            if room.room_name == room_name:
                print "\n"
                if room.occupants:
                    print "Office:", room.room_name
                    print "***************************"
                    for person in room.occupants:
                        print person.first_name, person.last_name
        for room in self.rooms["LivingSpace"]:
            if room.room_name == room_name:
                print "\n"
                if room.occupants:
                    print "LivingSpace:", room.room_name
                    print "***************************"
                    for person in room.occupants:
                        print person.first_name, person.last_name

            self.print_error("Add rooms to Amity")

    def print_allocations(self):
        try:
            for room in self.rooms["LivingSpace"]:
                print "\n"
                if room.occupants:
                    print "LivingSpace:", room.room_name
                    print "***************************"
                    for person in room.occupants:
                        print person.first_name, person.last_name

            for room in self.rooms["Office"]:
                print "\n"
                if room.occupants:
                    print "Office:", room.room_name
                    print "***************************"
                    for person in room.occupants:
                        print person.first_name, person.last_name
        except AttributeError:
            print "\n"

    def print_unallocated(self):
        open("unallocated.txt", "w").close()
        if not self.unallocated_persons:
            self.print_error("Existing persons have all been allocated")
        for person in self.unallocated_persons:
            self.print_success("\n{0} {1}".format(
                person.first_name, person.last_name))
            with open("unallocated.txt", "a") as myfile:
                myfile.write(person.first_name + " " + person.last_name +
                             " FELLOW" + " Y" + '\n')
                myfile.close()

    def load_people(self):
        r = open("txtfile.txt", "r")
        next = r.read().splitlines()
        try:
            for word in next:
                word = word.split(" ")
                words = list(word)
                first_name = words[0]
                last_name = words[1]
                person_type = words[2]

                if len(words) == 4:
                    self.add_person_fellow(first_name, last_name, person_type,
                                           words[3])
                elif len(words) <= 3:
                    self.add_person_staff(first_name, last_name, person_type,
                                          wants_space="N")
        except IndexError:
            self.print_error("\nCannot create user without person type")
            return 0
        self.print_success("\nPeople loaded successfully")

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

    def return_room_allocated(self, person_object):
        for room in self.rooms["LivingSpace"]:
            if person_object in room.occupants:
                return room
            else:
                return "\nPerson not allocated, check in unallocated lists"

    def print_success(self, text):
        cprint(text, 'green')

    def print_error(self, text):
        cprint(text, 'red')
