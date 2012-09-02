'''
Created on Sep 1, 2012

@author: pp
'''
class Table(object):
    def __init__(self, schema, idx, rows):
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

    def sort(self):
        pass
