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
