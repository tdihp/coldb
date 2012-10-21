import unittest
import random
from array import array

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


def _get_bytes(n_bytes):
    """random n_bytes generation"""
    return array('B', (random.randint(0, 255) for i in range(n_bytes))).tostring()


# algorithm mixins
class _TestGetMixin(object):
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
            l_data = self.compress_algo(self.col_type, l, **self.opts)
            col = self.colimpl(l_data, len(l))
            for i in range(length):
                self.assertEqual(l[i], col.get(i))


class _TestFindMixin(object):
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
            l_data = self.compress_algo(self.col_type, l, **self.opts)
            col = self.colimpl(l_data, length)
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
        self.opts = {}


class TestPlain_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'B'
        self.colimpl = colimpl.Plain_B
        self.opts = {}


class TestPlain_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'h'
        self.colimpl = colimpl.Plain_h
        self.opts = {}


class TestPlain_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'H'
        self.colimpl = colimpl.Plain_H
        self.opts = {}


class TestPlain_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'i'
        self.colimpl = colimpl.Plain_i
        self.opts = {}


class TestPlain_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_plain_normal
        self.col_type = 'I'
        self.colimpl = colimpl.Plain_I
        self.opts = {}


class TestRun0_b(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'b'
        self.colimpl = colimpl.Run0_bH
        self.opts = {'pt': 'H'}


class TestRun0_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'B'
        self.colimpl = colimpl.Run0_BH
        self.opts = {'pt': 'H'}


class TestRun0_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'h'
        self.colimpl = colimpl.Run0_hH
        self.opts = {'pt': 'H'}


class TestRun0_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'H'
        self.colimpl = colimpl.Run0_HH
        self.opts = {'pt': 'H'}


class TestRun0_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'i'
        self.colimpl = colimpl.Run0_iH
        self.opts = {'pt': 'H'}


class TestRun0_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run0
        self.col_type = 'I'
        self.colimpl = colimpl.Run0_IH
        self.opts = {'pt': 'H'}


class TestRun1_b(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-128, 128)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'b'
        self.colimpl = colimpl.Run1_bH
        self.opts = {'pt': 'H'}


class TestRun1_B(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 256)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'B'
        self.colimpl = colimpl.Run1_BH
        self.opts = {'pt': 'H'}


class TestRun1_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'h'
        self.colimpl = colimpl.Run1_hH
        self.opts = {'pt': 'H'}


class TestRun1_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'H'
        self.colimpl = colimpl.Run1_HH
        self.opts = {'pt': 'H'}


class TestRun1_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'i'
        self.colimpl = colimpl.Run1_iH
        self.opts = {'pt': 'H'}


class TestRun1_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.compress_algo = compress.c_run1
        self.col_type = 'I'
        self.colimpl = colimpl.Run1_IH
        self.opts = {'pt': 'H'}


class TestEnum_h(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-32768, 32768)
        self.lengthlist = [1, 10, 100]  # enum can't go up to 255
        self.compress_algo = compress.c_enum
        self.col_type = 'h'
        self.colimpl = colimpl.Enum_h
        self.opts = {}


class TestEnum_H(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 65536)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'H'
        self.colimpl = colimpl.Enum_H
        self.opts = {}


class TestEnum_i(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (-2 ** 31, 2 ** 31)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'i'
        self.colimpl = colimpl.Enum_i
        self.opts = {}


class TestEnum_I(unittest.TestCase, _TestGetMixin, _TestFindMixin):
    def setUp(self):
        self.datarange = (0, 2 ** 32)
        self.lengthlist = [1, 10, 100]
        self.compress_algo = compress.c_enum
        self.col_type = 'I'
        self.colimpl = colimpl.Enum_I
        self.opts = {}


class _TestStruct(object):
    """requires lengthlist, structlength, col_type, colimpl"""
    def testGet(self):
        for length in self.lengthlist:
            l = list(_get_bytes(self.structlength) for i in range(length))
            l_data = compress.c_plain_struct(self.col_type, l)
            col = self.colimpl(l_data, length)
            for i, val in enumerate(l):
                self.assertEqual(val, col.get(i))


class TestStruct_7(unittest.TestCase, _TestStruct):
    """struct7 is a test case to test the struct column"""
    def setUp(self):
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.structlength = 7
        self.col_type = '7s'
        self.colimpl = colimpl.Struct_7


class TestStruct_8(unittest.TestCase, _TestStruct):
    """struct7 is a test case to test the struct column"""
    def setUp(self):
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.structlength = 8
        self.col_type = '8s'
        self.colimpl = colimpl.Struct_8


class _TestBlob(object):
    """requires lengthlist, align, col_type, colimpl, slenrange
    """
    def testGet(self):
        for length in self.lengthlist:
            slens = (random.randint(*self.slenrange) for i in range(length))
            l = list(_get_bytes(self.align * slen) for slen in slens)
            l_data = compress.c_plain_blob(self.col_type, l, **self.opts)
            col = self.colimpl(l_data, length)
            for i, val in enumerate(l):
                self.assertEqual(val, col.get(i))


class TestBlob_1(unittest.TestCase, _TestBlob):
    def setUp(self):
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.align = 1
        self.col_type = 'blob1'
        self.colimpl = colimpl.Blob_1H
        self.slenrange = (0, 10)
        self.opts = {'bpt': 'H'}


class TestBlob_2(unittest.TestCase, _TestBlob):
    def setUp(self):
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.align = 2
        self.col_type = 'blob2'
        self.colimpl = colimpl.Blob_2H
        self.slenrange = (0, 10)
        self.opts = {'bpt': 'H'}


class TestBlob_4(unittest.TestCase, _TestBlob):
    def setUp(self):
        self.lengthlist = [1, 10, 100, 1000, 10000]
        self.align = 4
        self.col_type = 'blob4'
        self.colimpl = colimpl.Blob_4H
        self.slenrange = (0, 10)
        self.opts = {'bpt': 'H'}
