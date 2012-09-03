'''
Created on Sep 1, 2012

@author: pp
'''
from .common import col_uniname


def col_factory():
    pass


class Column(object):
    def __init__(self, schema, datatype, idx, tablename, name,):
        pass

    @property
    def schema(self):
        return self._schema

    def datatype(self):
        return self._datatype

    @property
    def tablename(self):
        return self._tablename

    @property
    def name(self):
        return self._name

    @property
    def uniname(self):
        return col_uniname(self.tablename, self.name)

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

    def minimum_type(self):
        """figure out the minimum data type needed to store the array"""


class StructColumn(Column):
    """ a simple buffer struct column """


class BlobColumn(Column):
    """ undetermined length blob col """
