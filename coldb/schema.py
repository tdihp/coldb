'''
Created on Sep 1, 2012

@author: pp
'''
import re

from .common import col_uniname, FKEY_RE, POINTER_TYPE
from .table import Table
from .column import Column


class Schema(object):
    def __init__(self, config):
        #read config
        #initial tables
        #use fkey to determine table sort order
        #sort and fkey translation
        #trying binary approaches
        self._tables = []
        self._cols = []
        self._read_config(config)
        self.validate()

    def __repr__(self):
        return "Schema(%s)" % (', '.join(self.table_by_name.keys()))

    @property
    def table_by_name(self):
        return dict((table.name, table) for table in self._tables)

    @property
    def col_by_uniname(self):
        return dict((col.uniname, col) for col in self._cols)

    def _read_config(self, config):
        fkey_pattern = re.compile(FKEY_RE)
        # read all tables
        for t_config in config['tables']:
            t_name = t_config['name']
            # make uninames
            if 'pkey' in t_config:
                t_config['pkey'] = col_uniname(t_name, t_config['pkey'])
            if 'skeys' in t_config:
                t_config['skeys'] = list(col_uniname(t_name, skey)\
                                         for skey in t_config['skeys'])

            t_config['col_uninames'] = []
            # read all columns
            for c_config in t_config['cols']:
                c_name = c_config['name']
                c_uniname = col_uniname(t_name, c_name)
                c_config['uniname'] = c_uniname
                c_config['tablename'] = t_config['name']
                t_config['col_uninames'].append(c_uniname)
                m = fkey_pattern.match(c_config['datatype'])
                if m:
                    c_config['datatype'] = POINTER_TYPE
                    c_config['fkey'] = m.groupdict()['target']
                if t_config.get('pkey', None) == c_uniname:
                    c_config['pkey'] = True
                self._cols.append(Column(self, **c_config))
            self._tables.append(Table(self, **t_config))

    def validate(self):
        """check all tables and columns"""
        for table in self._tables:
            table.validate()
        for col in self._cols:
            col.validate()
