import unittest
import sys
from StringIO import StringIO

from views.Amity import Amity


class TestAmity(unittest.TestCase):

    def setUp(self):
        """instance of amity created to pass class variables
        in Amity to test cases"""
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_create_room_and_add_room_successfully(self):
        # function tests if the create room method is adding rooms to lists
        # Create rooms which can offices or living spaces
        self.amity.create_room("Office", ["Hogwarts", "Krypton"])
        self.assertIn("Hogwarts", self.amity.get_roomname(
            self.amity.rooms["Office"]))

    def test_create_room_cannot_create_duplicate(self):
        # function tests if the create room method will accepted
        # chained duplicate names
        self.amity.create_room("LivingSpace", ["Java"])
        self.assertEqual("Java",
                         self.amity.get_roomobject("Java").room_name)
        self.amity.create_room("LivingSpace", ["Java"])
        output = sys.stdout.getvalue().strip()
        print output
        self.assertIn("Cannot create duplicate rooms", output)

    def test_get_roomname(self):
        # Create a room called Narnia
        self.amity.create_room('Office', ['Narnia'])
        # Call the get room name function
        self.assertIn("Narnia",
                      self.amity.get_roomname(self.amity.rooms["Office"]))

    def test_create_room_if_room_name_is_string(self):
        self.amity.create_room('Office', ['100'])
        output = sys.stdout.getvalue().strip()
        self.assertIn("Room name should be a string", output)

    def test_add_person(self):
        # Test fellow and staff are added to their respective lists
        first_name = "Martin"
        last_name = "Mungai"
        self.amity.add_person_fellow(first_name, last_name, 'FELLOW', 'Y')

        self.assertEqual("Martin",
                         self.amity.get_fellowobject(first_name,
                                                     last_name).first_name)
        self.amity.add_person_staff(first_name, last_name, 'STAFF', 'N')
        result2 = self.amity.get_staffobject(first_name, last_name)
        self.assertEqual(first_name, result2.first_name)

    def test_add_person_fellow_to_livingSpace(self):
        # create a room and add a fellow(s) to it
        self.amity.rooms["LivingSpace"] = []
        self.amity.create_room("LivingSpace", ["Go"])
        self.amity.add_person_fellow("Martin", "Mungai", 'FELLOW', "Y")
        result = self.amity.get_fellowobject("Martin", "Mungai")
        room_object = self.amity.get_roomobject(["Go"])
        for room in self.amity.rooms["LivingSpace"]:
            if room == room_object:
                return room
        self.assertIn(result.first_name, room.occupants[0].first_name)

    def test_add_person_staff_to_livingspace(self):
        self.amity.add_person_staff("Martin", "Mungai", "STAFF", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Staff not allowed to have living spaces", output)

    def test_allocate_persons(self):
        # Confirm people are being allocated
        self.amity.create_room("Office", ["Scala"])
        self.amity.add_person_fellow("Martin", "Mungai", "FELLOW", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Martin Mungai has been allocated", output)

    def test_reallocate_person_successfully(self):
        # Allocate person and reallocate the same person to another room
        first_name = "Martin"
        last_name = "Mungai"
        self.amity.create_room("LivingSpace", ["Python"])
        self.amity.add_person_fellow(first_name, last_name, "FELLOW", "Y")
        self.amity.create_room("LivingSpace", ["Narnia"])
        self.amity.reallocate_person(first_name, last_name, "FELLOW", "Narnia")
        result = self.amity.get_fellowobject(first_name, last_name)
        room_object = self.amity.get_roomobject(["Narnia"])
        for room in self.amity.rooms["LivingSpace"]:
            if room == room_object:
                print room
                self.assertIn(first_name, room.occupants)

    def test_print_room(self):
        self.amity.create_room("LivingSpace", ["Python"])
        self.amity.print_room("Python")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Python", output)


if __name__ == '__main__':
    unittest.main(exit=False)
