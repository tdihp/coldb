import struct
from cStringIO import StringIO

from .common import ALIGN_CHAR


def run(diff, col):
    if not len(col):
        return [], []
    last_val = col[0]
    vallist = [last_val]
    rowlist = [0]
    for cur_row, val in enumerate(col[1:], 1):
        if val - last_val != diff:
            vallist.append(val)
            rowlist.append(cur_row)
        last_val = val
    return rowlist, vallist


def enum(col):
    enumlist = sorted(set(col))
    enumdict = dict((val, i) for i, val in enumerate(enumlist))
    newvallist = list(enumdict[val] for val in col)
    return enumlist, newvallist


def align2pitch(inputlen, pitch):
    tail = inputlen % pitch
    return pitch - tail


def array_packing(arrdef, *more_arrdef):
    """pack mulltiple arrays into same str

    take care of alignments between arrays
    """
    arrtype, arr = arrdef
    last_bytes = struct.calcsize(arrtype)
    cur_size = last_bytes * len(arr)
    mybuffer = StringIO()
    mybuffer.write(struct.pack('%d%s' % (len(arr), arrtype), *arr))
    for arrtype, arr in more_arrdef:
        cur_bytes = struct.calcsize(arrtype)
        if cur_bytes > last_bytes:
            # align the string
            fill_bytes = align2pitch(cur_size, cur_bytes)
            mybuffer.write(ALIGN_CHAR * fill_bytes)
            cur_bytes += fill_bytes

            # write this arr
            cur_size = last_bytes * len(arr)
            mybuffer.write(struct.pack('%d%s' % (len(arr), arrtype), *arr))

            # leave notes
            last_bytes = cur_bytes
    rtn = mybuffer.getvalue()
    mybuffer.close()
    return rtn
