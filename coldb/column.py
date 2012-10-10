'''
Created on Sep 1, 2012

@author: pp
'''
import logging
from bisect import bisect_left

from .common import COMPRESS_TYPES
from .common import ALIGN_BYTES
from .common import uniname2name, is_blob_datatype, datatype2blob
from .common import BLOB_CTYPE2BPTR
from .compress import c_plain, c_run0, c_run1, c_enum
from .compress import CompressFailed
from .algorithm import minimum_type
from .algorithm import pitched_len
from .algorithm import ptr_type, bptr_type

COMPRESS_OPS = {
    'run0': c_run0,
    'run1': c_run1,
    'enum': c_enum,
}


class ColumnError(Exception):
    pass


class Column(object):
    def __init__(self, schema, uniname, datatype, tablename,
                 pkey=False, skey=False, fkey=None, compress=None, **kw):
        self._schema = schema
        self._uniname = uniname
        self._datatype = datatype
        self._tablename = tablename
        self._pkey = pkey
        self._skey = skey
        self._fkey = fkey
        self._compress = compress
        self.logger = logging.getLogger('coldb.column')

    @property
    def schema(self):
        return self._schema

    @property
    def uniname(self):
        return self._uniname

    @property
    def name(self):
        return uniname2name(self._uniname)

    @property
    def datatype(self):
        return self._datatype

    @property
    def tablename(self):
        return self._tablename

    @property
    def pkey(self):
        return self._pkey

    @property
    def skey(self):
        return self._skey

    @property
    def fkey(self):
        return self._fkey

    @property
    def compress(self):
        compress = self._compress
        if compress is None:
            return ()
        return compress

    def set_arr(self, arr):
        fkey = self.fkey
        if fkey:
            target_table = self.schema.table_by_name[fkey]
            target = self.schema.col_by_uniname[target_table.pkey]
            # target's arr must set already
            farr = []
            tarr = target.arr
            for val in arr:
                i = bisect_left(tarr, val)
                assert tarr[i] == val
                farr.append(i)
            self.arr = farr
        else:
            self.arr = arr

    def __repr__(self):
        return 'Column(%s)' % self.uniname

    def validate(self):
        # check fkey
        if self.fkey:
            ftable = self.schema.table_by_name[self.fkey]
            ftarget = self.schema.col_by_uniname[ftable.pkey]
            if ftarget.fkey:
                raise ColumnError("%s is fkey itself, cannot be targeted")

    def get_data(self):
        """returns colinfo block and data block"""
        arr = self.arr
        del self.arr
        min_type = minimum_type(self.datatype, arr)
        opts = {}
        #  get ptr type
        opts['pt'] = ptr_type(arr)
        #  get blob ptr type
        if is_blob_datatype(self.datatype):
            align = datatype2blob(self.datatype)
            opts['bpt'] = bptr_type(arr, align)
        cf, data = self.try_compress(min_type, arr, **opts)
        store_type = min_type
        if store_type not in ('b', 'B', 'h', 'H', 'i', 'I'):
            if 'bpt' in opts:
                store_type = BLOB_CTYPE2BPTR[opts['bpt']]
            else:
                store_type = '-'
        compression_id = COMPRESS_TYPES.index(cf)
        return store_type, compression_id, data

    def try_compress(self, val_type, arr, **opts):
        plain_data = c_plain(val_type, arr, **opts)
        comp_dict = dict()
        for cf in self.compress:
            try:
                comp_dict[cf] = COMPRESS_OPS[cf](val_type, arr, **opts)
            except CompressFailed as e:
                self.logger.info(e)
        comp_dict['plain'] = plain_data

        def compare(a, b):
            """smaller is better"""
            acf, acbin = a
            bcf, bcbin = b
            albin = len(acbin)
            blbin = len(bcbin)
            albin = pitched_len(albin, ALIGN_BYTES)
            blbin = pitched_len(blbin, ALIGN_BYTES)
            r = cmp(albin, blbin)
            if r:
                return r

            if acf == 'plain':
                return -1
            elif bcf == 'plain':
                return 1

            return 0

        min_cf, min_bin = sorted(((cf, cbin) for cf, cbin in comp_dict.items()),
            cmp=compare)[0]
        return min_cf, min_bin
