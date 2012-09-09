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
    """"""
    def __init__(self, schema, idx, name, col_idxes, pkey=None, skeys=None, **kw):
        """initial table, all cols should be idx"""
        self._schema = schema
        self._idx = idx
        self._name = name

        self._col_idxes = sorted(col_idxes)
        assert (not pkey) or (not skeys)
        self._pkey = pkey
        self._skeys = skeys

    @property
    def schema(self):
        return self._schema

    @property
    def idx(self):
        pass

    @property
    def name(self):
        pass

    @property
    def pkey(self):
        return self._pkey

    @property
    def col_idxes(self):
        return self._col_idxes

    @property
    def skeys(self):
        return self._skeys

    def feed_rows(self, rows):
        pass

    def catch_fkey(self):
        pass

    def sort_rows(self, rows):
#        sort_idxarr = list(for row in rows)
        sortcols = []
        if self.pkey:
            sortcols.append(self.pkey)
        if self.skeys:
            sortcols.extend(self.skeys)
        if not sortcols:
            return rows

        col_idxes = self.col_idxes
        idx_list = list(col_idxes.index(sidx) for sidx in sortcols)
        return sorted(rows, cmp=lambda a, b: _cmprow(idx_list, a, b))
