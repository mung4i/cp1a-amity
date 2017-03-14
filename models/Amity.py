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
        if person_type == "FELLOW":
            fellow = Fellow(person_name)
            self.people["FELLOWS"].append(fellow)
            if wants_space == "Y":
                allocated = random.choice(self.get_listofrooms())
                self.rooms["LivingSpace"][allocated].append(fellow)
        elif person_type == "STAFF":
            staff = Staff(person_name)
            self.people["STAFF"].append(staff)

    def get_personname(self):
        all_people = []
        for person in self.people["FELLOWS"]:
            all_people.append(person.name)
        return all_people

    def get_listofrooms(self):
        all_rooms = []
        #
        # for room in list(self.rooms["Office"].keys()):
        #     all_rooms.append(room.room_name)
        for room in list(self.rooms["LivingSpace"].keys()):
            if len(self.rooms["LivingSpace"][room]) < 4:
                all_rooms.append(room)
        return all_rooms

    def return_people_allocated(self):
        list_of_allocated = []
        for room in list(self.rooms["LivingSpace"].keys()):
            if len(self.rooms["LivingSpace"][room]) > 0:
                list_of_allocated.extend(self.rooms["LivingSpace"][room])
                for item in list_of_allocated:
                    peoples = []
                    peoples.append(item.name)
        return peoples

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

#
# amity = Amity()
# amity.create_room(["Java"], "LivingSpace")
# # amity.add_people("Martin Mungai", "FELLOW", "Y")
# # print amity.return_people_allocated()
# # print amity.get_personname()
# # amity.create_room(["Hogwarts"], "Office")
# # print amity.get_listofrooms()[0].room_name
