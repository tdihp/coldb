"""
Python range codec support, with correctness checks
"""
from coldb.rangecodec import REncoder, RDecoder, StrStream

FREQ_TOTAL = 1024

def countstr(input):
    """ count chars in string """
    cntarr = [0] * 256
    for c in input:
        cntarr[ord(c)] += 1
    cntdict = {}
    for i, c in enumerate(cntarr):
        if not c:
            continue
        cntdict[chr(i)] = c
    return cntdict

def entropy(cntdict, climit=256, total=FREQ_TOTAL):
    """
    order rule:
        most cnt at first
        prob limit at most climit
        prob minimum 1
    """
    uncounted = cntdict.copy()
    grandcnt = sum(cntdict.itervalues())
    entropydict = {}
    # deal with climit first
    for cchr, cnt in cntdict.iteritems():
        if (float(cnt) / float(grandcnt)) >= (float(climit) / float(total)):
            entropydict[cchr] = climit
            del uncounted[cchr]
    uncounted = sorted(((cchr, cnt) for cchr, cnt in uncounted.iteritems()),
                       key=lambda x: x[1])

    # deal with smaller freq first, for possible 0 to 1 happens
    for i in range(len(uncounted)):
        cchr, cnt = uncounted[i]
        grandcnt = sum(cnt for cchr, cnt in uncounted[i:])
        cur_total = total - sum(entropydict.itervalues())
        assert cur_total > 0
        ent = int(round(float(cnt) * float(cur_total) / float(grandcnt)))
        if ent < 1:
            ent = 1
        entropydict[cchr] = ent

    return entropydict

def entropy2tables(entropydict):
    # sort by key order
    ordered = sorted(entropydict.iteritems(), key=lambda x: ord(x[0]))
    ladder = [0]
    lchars = []
    char2i = {}
    lookup = []
    for i, (cchr, ent) in enumerate(ordered):
        char2i[cchr] = i
        lchars.append(cchr)
        ladder.append(ladder[i] + ent)
        lookup.extend([i] * ent)
    return ladder, lchars, char2i, lookup

def range_encode(input, ladder, lchars, char2i, lookup, decodecheck=True):
    buffer = StrStream("")
    encoder = REncoder(buffer)
    for c in input:
        i = char2i[c]
        encoder.enc(ladder[i], ladder[i + 1] - ladder[i])
    encoder.flush()
    encoded = buffer.getStr()[1:].rstrip("\0")
    # correctness check
    if decodecheck:
        decoded = range_decode(encoded,
                               ladder, lchars, char2i, lookup,
                               len(input))
        assert decoded == input
    return encoded

def range_decode(encoded, ladder, lchars, char2i, lookup, length):
    buffer = StrStream(encoded)
    decoder = RDecoder(buffer)
    decoded = []
    for i in range(length):
        mid = decoder.mid()
        i = lookup[mid]
        decoded.append(lchars[i])
        decoder.dec(ladder[i], ladder[i + 1] - ladder[i])
    return ''.join(decoded)
