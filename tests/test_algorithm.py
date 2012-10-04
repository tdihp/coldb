import unittest

from coldb import algorithm


class TestAlgorithm(unittest.TestCase):
    def testFrame(self):
        l = [1, 2, 3, 4, 1001, 1000, 1002, 1000, 50, 60, 70, 80]
        rowlist, framelist, newvallist = algorithm.frame(100, l)
        self.assertListEqual(rowlist, [0, 4, 8])
        self.assertListEqual(framelist, [1, 1000, 50])
        self.assertListEqual(newvallist, [0, 1, 2, 3, 1, 0, 2, 0, 0, 10, 20, 30])
