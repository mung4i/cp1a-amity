import unittest
import sys
from StringIO import StringIO
from cp1a.models.Amity import Amity


class TestAmity(unittest.TestCase):

    def setUp(self):
        """instance of amity created to pass class variables
        in Amity to test cases"""
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.create_room(["Java"], "LivingSpace")
        # for i in ["Martin", "Daniel", "Larry"]:
        #     self.new_fellow = Fellow(i)
        #     self.amity.people["FELLOWS"].append(self.new_fellow)

    def test_create_room_and_add_room_successfully(self):
        # function tests if the create room method is adding rooms to lists
        # Create rooms which can offices or living spaces
        self.amity.create_room(["Hogwarts", "Krypton"], "Office")
        self.assertIn("Hogwarts", self.amity.get_roomname(
            list(self.amity.rooms["Office"].keys())))

    def test_create_room_cannot_create_duplicate(self):
        # function tests if the create room method will accepted
        # chained duplicate names
        target = "Java"
        self.amity.create_room([target], "LivingSpace")
        self.assertIn(target, self.amity.get_roomname(
            list(self.amity.rooms["LivingSpace"].keys())))
        self.amity.create_room([target], "LivingSpace")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Cannot create duplicate rooms", output)

    def test_get_roomname(self):
        # Create a room called Narnia
        self.amity.create_room(['Narnia'], 'Office')
        # Call the get room name function
        self.assertIn("Narnia",
                      self.amity.get_roomname(
                          list(self.amity.rooms["Office"].keys())))

    def test_create_room_if_room_name_is_string(self):
        self.amity.create_room([100], 'Office')
        output = sys.stdout.getvalue().strip()
        self.assertIn("Room name should be a string", output)

    def test_add_person(self):
        # Test fellow and staff are added to their respective lists
        self.amity.add_people("Martin", 'FELLOW', 'Y')
        self.assertIn("Martin", self.amity.get_personname())
        self.amity.add_people("Martin", 'STAFF', 'N')
        self.assertIn("Martin", self.amity.get_personname())

    def test_add_person_fellow_to_livingSpace(self):
        # create a room and add a fellow(s) to it
        self.amity.create_room(["Go"], "LivingSpace")
        person_name = 'Daniel'
        self.amity.add_people([person_name], 'FELLOW', "Y")
        self.assertIn(["Daniel"], self.amity.return_people_allocated()[1])

    def test_add_person_staff_to_livingspace(self):
        self.amity.add_people("Martin", 'STAFF', "Y")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Staff not allowed to have living spaces", output)

    def test_allocate_persons(self):
        # Confirm people are being allocated
        self.amity.add_people("Martin", "FELLOW", "Y")
        self.assertIn("Martin", self.amity.return_people_allocated()[1])

    def test_reallocate_person_successfully(self):
        # Allocate person and reallocate the same person to another room
        self.amity.create_room(["Python"], "LivingSpace")
        self.amity.add_people("Martin", "FELLOW", "Y")
        self.assertIn("Martin", self.amity.return_people_allocated()[1])

    def test_print_rooms(self):
        self.assertTrue(self.amity.print_rooms(), msg="Rooms were not printed")

    if __name__ == '__main__':
        unittest.main()
