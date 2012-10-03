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


# algorithm mixins
class _TestGetMixin():
    """ requires these attributes:

    - datarange: range of auto generated data
    - lengthlist: a list of lengths of array data
    - compress_algo: the compress algorithm to be used
    - col_type: compress_algo's col_type param
    - colimpl: impl class
    """
    def testGet(self):
        for length in self.lengthlist:
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
        for length in self.lengthlist:
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
#                self.assertEqual(i, col.find(cur_data), "%d, %d, %d, %s" % (i, col.find(cur_data), cur_data, l))
                self.assertEqual(i, col.find(cur_data))
                last_data = cur_data


class TestPlain_b(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'b'
        self.colimpl = colimpl.Plain_b


class TestPlain_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'B'
        self.colimpl = colimpl.Plain_B


class TestPlain_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'h'
        self.colimpl = colimpl.Plain_h


class TestPlain_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'H'
        self.colimpl = colimpl.Plain_H


class TestPlain_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'i'
        self.colimpl = colimpl.Plain_i


class TestPlain_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'I'
        self.colimpl = colimpl.Plain_I


class TestRun0_b(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'b'
        self.colimpl = colimpl.Run0_b


class TestRun0_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'B'
        self.colimpl = colimpl.Run0_B


class TestRun0_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'h'
        self.colimpl = colimpl.Run0_h


class TestRun0_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'H'
        self.colimpl = colimpl.Run0_H


class TestRun0_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'i'
        self.colimpl = colimpl.Run0_i


class TestRun0_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'I'
        self.colimpl = colimpl.Run0_I


class TestRun1_b(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'b'
        self.colimpl = colimpl.Run1_b


class TestRun1_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'B'
        self.colimpl = colimpl.Run1_B


class TestRun1_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'h'
        self.colimpl = colimpl.Run1_h


class TestRun1_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'H'
        self.colimpl = colimpl.Run1_H


class TestRun1_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'i'
        self.colimpl = colimpl.Run1_i


class TestRun1_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'I'
        self.colimpl = colimpl.Run1_I


class TestEnum_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'h'
        self.colimpl = colimpl.Enum_h


class TestEnum_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'H'
        self.colimpl = colimpl.Enum_H


class TestEnum_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'i'
        self.colimpl = colimpl.Enum_i


class TestEnum_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'I'
        self.colimpl = colimpl.Enum_I
