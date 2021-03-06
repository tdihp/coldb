from struct import Struct
from cStringIO import StringIO

from .common import ALIGN_CHAR
from .common import IRANGE_DICT


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


def frame(fsize, col):
    """fsize: a size of the frame. fmax-fmin < fsize"""
    framelist = []
    rowlist = []
    newvallist = []
    cur_min = col[0]
    cur_max = col[0]
    cur_startrow = 0
    for cur_row, val in enumerate(col[1:], 1):
        if(cur_min <= val <= cur_max):
            continue
        new_min = cur_min
        new_max = cur_max
        if val < new_min:
            new_min = val
        if val > new_max:
            new_max = val
        if new_max - new_min >= fsize:
            # emit a frame
            framelist.append(cur_min)
            rowlist.append(cur_startrow)
            # start a new frame
            cur_startrow = cur_row
            cur_min = val
            cur_max = val
        else:
            cur_min = new_min
            cur_max = new_max
    # emit the final frame
    framelist.append(cur_min)
    rowlist.append(cur_startrow)
    # now, the val list
    for i, (frame, row) in enumerate(zip(framelist, rowlist)[:-1]):
        newvallist.extend(list((val - frame) for val in col[row:rowlist[i + 1]]))

    newvallist.extend(list(val - framelist[-1] for val in col[rowlist[-1]:]))
    return rowlist, framelist, newvallist


def align2pitch(inputlen, pitch):
    tail = inputlen % pitch
    if tail:
        return pitch - tail
    return 0


def pitched_len(inputlen, pitch):
    return inputlen + align2pitch(inputlen, pitch)


def array_packing(arrdef, *more_arrdef):
    """pack mulltiple arrays into same str

    take care of alignments between arrays
    """
    arrtype, arr = arrdef
    mystruct = Struct(arrtype)
    last_bytes = mystruct.size
    cur_size = last_bytes * len(arr)
    mybuffer = StringIO()
    mybuffer.write(''.join(mystruct.pack(val) for val in arr))
    for arrtype, arr in more_arrdef:
        mystruct = Struct(arrtype)
        cur_bytes = mystruct.size
        if cur_bytes > last_bytes:
            # align the string
            fill_bytes = align2pitch(cur_size, cur_bytes)
            mybuffer.write(ALIGN_CHAR * fill_bytes)
            cur_bytes += fill_bytes

        # write this arr
        cur_size = last_bytes * len(arr)
        mybuffer.write(''.join(mystruct.pack(val) for val in arr))

        # leave notes
        last_bytes = cur_bytes

    rtn = mybuffer.getvalue()
    mybuffer.close()
    return rtn


def _compare_type(dmin, dmax, comptypes, default=None):
    for t in comptypes:
        tmin, tmax = IRANGE_DICT[t]
        if tmin <= dmin and dmax <= tmax:
            return t
    assert not default is None, 'No type fits!'
    return default


def minimum_type(default_type, col_data):
    """figure out the minimum data type needed to store the array"""
    dmin = min(col_data)
    dmax = max(col_data)
    conv_table = {
        'b': '',
        'B': '',
        'h': 'b',
        'H': 'B',
        'i': 'bh',
        'I': 'BH',
    }
    dt = default_type
    if not dt in conv_table:
        return dt
    test_ts = conv_table[dt]
    return _compare_type(dmin, dmax, test_ts, dt)


def ptr_type(col_data):
    """ figure out which datatype do be used as ptr """
    l = len(col_data)
    ptr_conv_order = 'BHI'
    return _compare_type(0, l, ptr_conv_order)


def bptr_type(blob_col_data, align):
    _sum = 0
    for d in blob_col_data:
        _div, _mod = divmod(len(d), align)
        assert not _mod
        _sum += _div
    ptr_conv_order = 'HI'
    return _compare_type(0, _sum, ptr_conv_order)


def make_aligned_blocks(pitch, *blocks):
    mybuffer = StringIO()
    cur_size = 0
    for block in blocks:
        align = align2pitch(cur_size, pitch)
        if align:
            mybuffer.write(ALIGN_CHAR * align)
            cur_size += align
        mybuffer.write(block)
        cur_size += len(block)
    result = mybuffer.getvalue()
    mybuffer.close()
    return result
