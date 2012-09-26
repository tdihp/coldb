'''
Created on Sep 2, 2012

@author: pp
'''
import re

ALIGN_BYTES = 4
ALIGN_CHAR = '\0'


# indicate sizes, pointing rows, size_counting
POINTER_TYPE = 'H'

# used in enum compression only
ENUM_TYPE = 'B'

# XXX: not used
IDX_TYPE = 'H'

# header uses 2 magic words
S_PACKAGE_HEADER_STRUCT = 'HH'
# rows
S_TABLE_HEADER_STRUCT = 'H'
# data_type, compress_type, size *ALIGN_BYTES to bytes*
# data_type:
# same as struct if the type changed
# '-' if no change at all
S_COL_HEADER_STRUCT = 'cBH'


IRANGE_DICT = {
    'b': (-128, 127),
    'B': (0, 255),
    'h': (-32768, 32767),
    'H': (0, 65535),
    'i': (-2147483648, 2147483647),
    'I': (0, 4294967295),
}

COMPRESS_TYPES = [
    'plain',
    'run0',
    'run1',
    'enum',
]

DATATYPE2CTYPE = {
    'b': 'I8',
    'B': 'U8',
    'h': 'I16',
    'H': 'U16',
    'i': 'I32',
    'I': 'U32',
}

FKEY_RE = r'fkey\((?P<target>\w+)\)'


def col_uniname(tablename, colname):
    return tablename + '__' + colname
    
def uniname2name(uniname):
    return uniname.split('__')[-1]

def is_struct_datatype(datatype):
    return re.match(r'^(?P<size>\d+)s$', datatype)

def is_blob_datatype(datatype):
    return re.match(r'^blob(?P<align>\d+)$')

def datatype2struct(datatype):
    m = is_struct_datatype(datatype)
    size = int(m.groupdict()['size'])
    assert size > 0
    return size
    
def datatype2blob(datatype):
    m = is_blob_datatype(datatype)
    align = int(m.groupdict()['align'])
    assert align in (1, 2, 4)
    return align
    