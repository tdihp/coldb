'''
Created on Sep 2, 2012

@author: pp
'''
ALIGN_BYTES = 4
ALIGN_CHAR = '\0'


# indicate sizes, pointing rows, size_counting
POINTER_TYPE = 'H'

# XXX: not used
IDX_TYPE = 'H'

# rows
S_TABLE_HEADER_STRUCT = 'H'
# data_type, compress_type, size(* ALIGN_BYTES to bytes)
# data_type: 
# same as struct if the type changed
# '-' if no change at all
S_COL_HEADER_STRUCT = 'BBH'

# compress types
COMPRESS_TYPE_PLAIN = 0
COMPRESS_TYPE_SAME = 1
COMPRESS_TYPE_PROGRESS = 2
COMPRESS_TYPE_ENUM = 3

IRANGE_DICT = {
    'b': (-128, 127),
    'B': (0, 255),
    'h': (-32768, 32767),
    'H': (0, 65535),
    'l': (-2147483648, 2147483647),
    'L': (0, 4294967295),
}

COMPRESS_DICT = {
    None: COMPRESS_TYPE_PLAIN,
    'plain': COMPRESS_TYPE_PLAIN,
    'same': COMPRESS_TYPE_SAME,
    'progress': COMPRESS_TYPE_PROGRESS,
    'enum': COMPRESS_TYPE_ENUM,
}


def col_uniname(tablename, colname):
    return tablename + '__' + colname




