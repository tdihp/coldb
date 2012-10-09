'''
Created on Sep 1, 2012

@author: pp
'''
import re
from struct import Struct
import logging
from .common import S_TABLE_HEADER_STRUCT, S_COL_HEADER_STRUCT, S_PACKAGE_HEADER_STRUCT
from .common import col_uniname, FKEY_RE, POINTER_TYPE, ALIGN_BYTES
from .table import Table
from .column import Column
from .algorithm import pitched_len, align2pitch, make_aligned_blocks

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
        self.logger = logging.getLogger('coldb.schema')

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
                if 'skeys' in t_config:
                    if c_uniname == t_config['skeys'][0]:
                        c_config['skey'] = True
                self._cols.append(Column(self, **c_config))
            self._tables.append(Table(self, **t_config))

    def validate(self):
        """check all tables and columns"""
        for table in self._tables:
            table.validate()
        for col in self._cols:
            col.validate()

    def make_data(self, data):
        tabledict = self.table_by_name
        coldict = self.col_by_uniname
        # for tablename, rows in data.items():
            # assert tablename in tabledict
            # tabledict[tablename].set_rows(rows)

        for table in self._tables:
            tablename = table.name
            table.set_rows(data[tablename])

        package_header_struct = Struct(S_PACKAGE_HEADER_STRUCT)
        table_header_struct = Struct(S_TABLE_HEADER_STRUCT)
        col_header_struct = Struct(S_COL_HEADER_STRUCT)

        table_header_list = []
        col_header_list = []
        col_data_list = []

        for table in self._tables:
            table_len = table.get_data()
            table_header_list.append(table_header_struct.pack(table_len))
            if table_len:
                for col_uniname in table.col_uninames:
                    col = coldict[col_uniname]
                    store_type, compression_id, data = col.get_data()
                    col_size = pitched_len(len(data), ALIGN_BYTES)
                    col_header_list.append(col_header_struct.pack(store_type, compression_id))
                    col_data_list.append(data)
                    self.logger.info("%s, %s, %s, %s", col_uniname, store_type, compression_id, col_size)
        package_header = package_header_struct.pack(0, 0)
        table_header_struct = ''.join(table_header_list)
        col_header_struct = ''.join(col_header_list)
        return make_aligned_blocks(ALIGN_BYTES, package_header, table_header_struct, col_header_struct, *col_data_list)
