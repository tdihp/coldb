'''
Created on Sep 1, 2012

@author: pp
'''
from .common import col_uniname


def _cmprow(idxarr, row1, row2):
    for idx in idxarr:
        c = cmp(row1[idx], row2[idx])
        if c:
            return c
    return 0


class Table(object):
    def __init__(self, schema, idx, col_uninames, pkey=None, skeys=None):
        self._schema = schema
        self._idx = idx


        self._cols = list((schema.col_by_uniname[col_uniname].idx, col_uniname, schema.col_by_uniname[col_uniname]) for col_uniname in col_uninames)
        cols = []
        for col_uniname in col_uninames:
            col = schema.col_by_uniname[col_uniname]
            cols.append(col)
        cols = sorted(cols, key=col.idx)

    @property
    def schema(self):
        pass

    @property
    def pkey(self):
        pass

    @property
    def skeys(self):
        pass

    @property
    def name(self):
        pass

    @property
    def idx(self):
        pass

    def feed_rows(self, rows):
        pass

    def catch_fkey(self):
        pass

    def sort_rows(self, rows):
#        sort_idxarr = list(for row in rows)
        pass
