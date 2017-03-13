import unittest
from cp1a.models.Amity import Amity
from cp1a.models.Fellow import Fellow


class TestAmity(unittest.TestCase):

    def setUp(self):
        """instance of amity created to pass class variables
        in Amity to test cases"""
        self.amity = Amity()

        for i in ["Martin", "asdas", "asdgfdg"]:
            self.new_fellow = Fellow(i)
            self.amity.people["FELLOWS"].append(self.new_fellow)

    def test_create_room_and_add_room_successfully(self):
        # function tests if the create room method is adding rooms to lists
        # Create rooms which can offices or living spaces
        self.amity.create_room(["Java", "Python"], 'LivingSpace')
        self.assertIn("Java", self.amity.rooms['LivingSpace'],
                      msg="Rooms were not created")
