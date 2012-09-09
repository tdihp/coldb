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
    def __init__(self, schema, name, col_uninames, pkey=None, skeys=None, **kw):
        """initial table, all cols should be idx

        col_uninames is also used to indicate row data order
        all column properties uses uniname
        """
        self._schema = schema
        self._name = name

        self._col_uninames = col_uninames
        assert (not pkey) or (not skeys)
        self._pkey = pkey
        self._skeys = skeys

    @property
    def schema(self):
        return self._schema

    @property
    def name(self):
        return self._name

    @property
    def col_uninames(self):
        return self._col_uninames

    @property
    def pkey(self):
        return self._pkey

    @property
    def skeys(self):
        return self._skeys

    def feed_rows(self, rows):
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

        col_uninames = self.col_uninames
        idx_list = list(col_uninames.index(snames) for snames in sortcols)
        return sorted(rows, cmp=lambda a, b: _cmprow(idx_list, a, b))
