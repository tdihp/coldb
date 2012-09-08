'''
Created on Sep 1, 2012

@author: pp
'''
from .common import col_uniname
from .common import IRANGE_DICT
from .compress import c_plain, c_run0, c_run1, c_enum


COMPRESS_OPS = {
    'run0': c_run0,
    'run1': c_run1,
    'enum': c_enum,
}


def _compare_type(dmin, dmax, comptypes, default):
    for t in comptypes:
        tmin, tmax = IRANGE_DICT[t]
        if tmin <= dmin and dmax <= tmax:
            return t
    return default


def col_factory():
    pass


class Column(object):
    def __init__(self, schema, idx, datatype, tablename, uniname,
                 compress=None):
        pass

    @property
    def schema(self):
        return self._schema

    @property
    def datatype(self):
        return self._datatype

    @property
    def tablename(self):
        return self._tablename

    @property
    def name(self):
        return self.uniname

    @property
    def idx(self):
        pass

    def write_data(self, arr):
        pass

    def try_compress(self):
        pass


class SimpleColumn(Column):
    """ col for simple data types """
    def compress(self, method):
        pass

    def minimum_type(self, col_data):
        """figure out the minimum data type needed to store the array"""
        dmin = min(col_data)
        dmax = max(col_data)
        conv_table = {
            'b': '',
            'B': '',
            'h': 'b',
            'H': 'B',
            'l': 'bh',
            'L': 'BH',
        }
        dt = self.datatype
        assert dt in conv_table
        test_ts = conv_table[dt]
        return _compare_type(dmin, dmax, test_ts, dt)

class StructColumn(Column):
    """ a simple buffer struct column """
    def minimum_type(self, col_data):
        return '-'

class BlobColumn(Column):
    """ undetermined length blob col """
    def minimum_type(self, col_data):
        return '-'
