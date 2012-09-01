import logging


def col_uniname(tablename, colname):
    return tablename + '__' + colname


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


def col_factory():
    pass

class Column(object):
    def __init__(self, schema, idx, tablename, name):
        pass

    @property
    def schema(self):
        return self._schema

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


class FColumn(SimpleColumn):
    def __init__(self, *args, **kwargs):
        super(FColumn, self).__init__(*args, **kwargs)



def makedb(schema, table_mapping):


    # for each table
    pass
