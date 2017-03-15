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
        for room in room_names_list:
            if not type(room) == str:
                print "Room name should be a string"
                break
            if room in self.get_roomname(
                    list(self.rooms["LivingSpace"].keys())):
                print "Cannot create duplicate rooms"
                break
            if room in self.get_roomname(
                    list(self.rooms["Office"].keys())):
                print "Cannot create duplicate rooms"
                break
            if room_type == "LivingSpace":
                for lspacename in room_names_list:
                    livingspace = LivingSpace(lspacename)
                    self.rooms["LivingSpace"][livingspace] = []
                    print "Room {0} successfuly created".format(
                        livingspace.room_name)
            if room_type == "Office":
                for ospacename in room_names_list:
                    office = Office(ospacename)
                    self.rooms["Office"][office] = []
                    print "Room {0} successfuly created".format(
                        office.room_name)

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
            if wants_space == "Y":
                print "Staff not allowed to have living spaces"

    def get_personobject(self, person_name):
        for person_name in self.people["FELLOWS"]:
            fellow_object = person_name
        return fellow_object

    def get_personname(self):
        all_people = []
        for person in self.people["FELLOWS"]:
            all_people.append(person.name)
        return all_people

    def get_listofrooms(self):
        all_rooms = []
        for room in list(self.rooms["LivingSpace"].keys()):
            if len(self.rooms["LivingSpace"][room]) < 4:
                all_rooms.append(room)
        return all_rooms

    def return_people_allocated(self):
        list_of_allocated = []
        peoples = []
        fellow_objects = []
        for room in list(self.rooms["LivingSpace"].keys()):
            if len(self.rooms["LivingSpace"][room]) > 0:
                list_of_allocated.extend(self.rooms["LivingSpace"][room])
                for item in list_of_allocated:
                    fellow_objects.append(item)
                    peoples.append(item.name)
        return fellow_objects, peoples

    def return_room_allocated(self, person_object):
        room_object = []
        for room in list(self.rooms["LivingSpace"].keys()):
            if person_object in self.rooms["LivingSpace"][room]:
                room_object.append(room)
                return room_object, room

    def deallocate_fellow(self, person_object, room_object):
        if person_object in self.rooms["LivingSpace"][room_object]:
            self.rooms["LivingSpace"][room_object].remove(person_object)
        else:
            return "{0} not in {1}".format(
                person_object.name, room_object.room_name)

    def reallocatePerson(self, person_name, person_type, wants_space="Y"):
        if person_type == "FELLOW":
            target = self.get_personobject(person_name)
            assigned = self.return_room_allocated(target)[1]
            self.deallocate_fellow(target, assigned)
            if wants_space == "Y":
                allocated = random.choice(self.get_listofrooms())
                self.rooms["LivingSpace"][allocated].append(target)
                print "successfuly reallocated"

    def print_rooms(self):
        room_names_list = []
        rooms = self.get_listofrooms()
        for room in rooms:
            room_names_list.append(room.room_name)
        return room_names_list

    def print_allocations(self, ):
        pass

    def print_unallocated(self, ):
        pass

    def save_state(self, ):
        pass

    def load_state(self, ):
        pass
