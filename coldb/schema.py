'''
Created on Sep 1, 2012

@author: pp
'''
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

    @property
    def table_by_name(self):
        pass

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
        for t_name, t_config in config['tables'].items():
            self.add_table(t_name, t_config)


    def add_table(self, t_name, t_config):
        assert t_name not in self.table_by_name
        t_config = t_config.copy()
        t_config['idx'] = self.gen_idx()
        t_config['name'] = t_name
        t = Table(self, **t_config)
        self._tables.append(t)

    def add_column(self, t_name, c_name, c_config):
        pass

    def gen_idx(self):
        self._current_idx += 1
        return self._current_idx
