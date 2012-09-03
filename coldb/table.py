'''
Created on Sep 1, 2012

@author: pp
'''


def _cmprow(idxarr, row1, row2):
    for idx in idxarr:
        c = cmp(row1[idx], row2[idx])
        if c:
            return c
    return 0


class Table(object):
    def __init__(self, schema, idx, colnames, pkey=None, skeys=None):
        self._schema = schema
        self._idx = idx

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

    def catch_fkey(self):
        pass

    def sortrows(self):
        pass
