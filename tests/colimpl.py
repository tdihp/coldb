import unittest
import random

from coldb import compress
from coldb import colimpl


def _get_data(length, drange):
    """ return a list of randomized data """
    _min, _max = drange
    return list(random.randint(_min, _max - 1) for i in range(length))


def _get_sorted_data(length, drange):
    """ return a random sorted list
    """
    result = _get_data(length, drange)
    return sorted(result)


def _get_unique_sorted(length, drange):
    return sorted(random.sample(xrange(*drange), length))


# algorithm mixins
class _TestGetMixin():
    """ requires these attributes:

    - datarange: range of auto generated data
    - get_lengthlist: a list of lengths of array data
    - compress_algo: the compress algorithm to be used
    - col_type: compress_algo's col_type param
    - colimpl: impl class
    """
    def testGet(self):
        for length in self.get_lengthlist:
            l = _get_data(length, self.datarange)
            l_data = self.compress_algo(self.col_type, l)
            col = self.colimpl(l_data, len(l))
            for i in range(length):
                self.assertEqual(l[i], col.get(i))


class _TestFindMixin():
    """ requires these attributes:

    - datarange: range of auto generated data
    - find_lengthlist: a list of lengths of array data
    - compress_algo: the compress algorithm to be used
    - col_type: compress_algo's col_type param
    - colimpl: impl class
    """
    def testFind(self):
        for length in self.find_lengthlist:
            l = _get_sorted_data(length, self.datarange)
            l_data = self.compress_algo(self.col_type, l)
            col = self.colimpl(l_data, len(l))

            # test find first
            cur_data = l[0]
            self.assertEqual(0, col.find(cur_data))
            last_data = cur_data
            for i, cur_data in enumerate(l[1:], 1):
                if cur_data == last_data:
                    continue
                self.assertEqual(i, col.find(cur_data))
                last_data = cur_data


class TestPlain_b(unittest.TestCase, _TestGetMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.get_lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'b'
        self.colimpl = colimpl.Plain_b

    def tearDown(self):
        pass


class TestPlain_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.get_lengthlist = [1, 10, 100, 1000, 10000]
        self.find_lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'B'
        self.colimpl = colimpl.Plain_B

    def tearDown(self):
        pass


class TestPlain_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.get_lengthlist = [1, 10, 100, 1000, 10000]
        self.find_lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'H'
        self.colimpl = colimpl.Plain_H

    def tearDown(self):
        pass
