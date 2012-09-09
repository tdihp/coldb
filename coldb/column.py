'''
Created on Sep 1, 2012

@author: pp
'''
from .common import IRANGE_DICT
from .common import COMPRESS_TYPES
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
    def __init__(self, schema, uniname, datatype, tablename,
                 pkey=False, fkey=None, compress=None, **kw):
        self._schema = schema
        self._uniname = uniname
        self._datatype = datatype
        self._tablename = tablename
        self._pkey = pkey
        self._fkey = fkey

    @property
    def schema(self):
        return self._schema

    @property
    def uniname(self):
        return self._uniname

    @property
    def datatype(self):
        return self._datatype

    @property
    def tablename(self):
        return self._tablename

    @property
    def pkey(self):
        return self._pkey

    @property
    def fkey(self):
        return self._fkey

    @property
    def compress(self):
        return self._compress

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
        if not dt in conv_table:
            return dt
        test_ts = conv_table[dt]
        return _compare_type(dmin, dmax, test_ts, dt)

    def write_data(self, arr):
        """returns colinfo block and data block"""
        min_type = self.minimum_type(arr)
        cf, data = self.try_compress(min_type, arr)
        store_type = min_type
        if store_type not in ('b', 'B', 'h', 'H', 'l', 'L'):
            store_type = '-'
        compression_id = COMPRESS_TYPES.index(cf)
        return store_type, compression_id, data

    def try_compress(self, val_type, arr):
        plain_data = c_plain(val_type, arr)
        comp_dict = dict()
        for cf in self.compress:
            comp_dict[cf] = COMPRESS_OPS[cf](val_type, arr)
        comp_dict['plain'] = plain_data
        min_cf, min_bin = min(((cf, cbin) for cf, cbin in comp_dict.items()),
            key=lambda c, b: len(b))
        return min_cf, min_bin