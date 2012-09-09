'''
Created on Sep 1, 2012

@author: pp
'''
from .common import col_uniname
from .table import Table
from .column import Column


class Schema(object):
    def __init__(self, config):
        #read config
        #initial tables
        #use fkey to determine table sort order
        #sort and fkey translation
        #trying binary approaches
        self._current_idx = 0
        self._tables = []
        self._cols = []
        self._read_config(config)

    @property
    def table_by_name(self):
        return dict((table.name, table) for table in self._tables)

    @property
    def table_by_idx(self):
        pass

    @property
    def col_by_uniname(self):
        pass

    @property
    def col_by_idx(self):
        pass

    def _read_config(self, config):
        for t_config in config['tables']:
            self.add_table(t_config)

    def add_table(self, t_config):
#        assert t_name not in self.table_by_name
        t_name = t_config['name']
        t_config['idx'] = self.gen_idx()
        t_config['col_idxes'] = []
        for c_config in t_config['cols']:
            c_config['idx'] = self.gen_idx()
            c_name = c_config['name']
            col_uniname(t_name, c_name)
            c_config['uniname'] = col_uniname(t_name, c_name)
            c_config['tableidx'] = t_config['idx']
            c = Column(self, **c_config)
            t_config['col_idxes'].append(c_config['idx'])
            self._cols.append(c)

        t = Table(self, **t_config)
        self._tables.append(t)

    def add_column(self, t_name, c_name, c_config):
        pass

    def gen_idx(self):
        self._current_idx += 1
        return self._current_idx
