'''
Created on Sep 8, 2012

@author: pp
'''
import re
import struct
from cStringIO import StringIO

from .algorithm import run, enum, array_packing
from .common import POINTER_TYPE, ENUM_TYPE


class CompressFailed(Exception):
    pass


def c_plain(col_type, col):
    """ the default non-compression approach """
    if col_type in ('b', 'B', 'h', 'H', 'l', 'L'):
        return c_plain_normal(col_type, col)
    elif re.match(r'^\d+s$', col_type):
        return c_plain_struct(col_type, col)
    elif 'blob' == col_type:
        return c_plain_blob(col_type, col)


def c_plain_normal(col_type, col):
    assert col_type in ('b', 'B', 'h', 'H', 'l', 'L')
    return array_packing((col_type, col))


def c_plain_struct(col_type, col):
    assert re.match(r'^\d+s$', col_type)
    mystruct = struct.Struct(col_type)
    return ''.join(mystruct.pack(val) for val in col)


def c_plain_blob(col_type, col):
    assert 'blob' == col_type
    start_list = []
    cnt_list = []
    mybuffer = StringIO()
    cur_pos = 0
    for val in col:
        l = len(val)
        start_list.append(cur_pos)
        cnt_list.append(l)
        mybuffer.write(val)
        cur_pos += l
    mybuffer_val = mybuffer.getvalue()
    mybuffer.close()
    mybuffer_len = len(mybuffer_val)
    result = array_packing((POINTER_TYPE,
                            [mybuffer_len] + start_list + cnt_list))
    return result + mybuffer_val


def c_run0(col_type, col):
    assert col_type in ('b', 'B', 'h', 'H', 'l', 'L')
    rowlist, vallist = run(0, col)
    rowcnt = len(rowlist)
    result = array_packing((POINTER_TYPE, [rowcnt] + rowlist),
                           (col_type, vallist))
    return result


def c_run1(col_type, col):
    assert col_type in ('b', 'B', 'h', 'H', 'l', 'L')
    rowlist, vallist = run(1, col)
    rowcnt = len(rowlist)
    result = array_packing((POINTER_TYPE, [rowcnt] + rowlist),
                           (col_type, vallist))
    return result


def c_enum(col_type, col):
    assert col_type in ('h', 'H', 'l', 'L')  # enum of bytes is useless
    enumlist, newvallist = enum(col)
    enumcnt = len(enumlist)
    result = array_packing((ENUM_TYPE, [enumcnt] + newvallist),
                           (col_type, enumlist))
    return result
