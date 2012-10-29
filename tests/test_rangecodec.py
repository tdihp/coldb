from coldb.rangecodec import REncoder, RDecoder, StrStream

def entropy(cntdict, climit=512, total=1024):
    """
    order rule:
        most cnt at first
        if prob equal, use alphabet order
        prob limit at most climit
        prob minimum 1
    """
    uncounted = cntdict.copy()
    grandcnt = sum(cntdict.itervalues())
    entropydict = {}
    # deal with climit first
    for chr, cnt in cntdict.iteritems():
        if (cnt / grandcnt) > (climit / total):
            entropydict[chr] = climit
            del uncounted[chr]
    uncounted = sorted(((chr, cnt) for chr, cnt in uncounted.iteritems()),
                       key=lambda x: x[1])

    for i in range(len(uncounted)):
        chr, cnt = uncounted[i]
        grandcnt = sum(cnt for chr, cnt in uncounted[i:])
        cur_total = total - sum(entropydict.itervalues())
        assert cur_total > 0
        ent = int(round(cnt * cur_total / grandcnt))
        if ent < 1:
            ent = 1
        entropydict[chr] = ent

    return entropydict


def entropy2tables(entropydict):
    def cmpchrent(chrent1, chrent2):
        chr1, ent1 = chrent1
        chr2, ent2 = chrent2
        c1 = cmp(ent1, ent2)
        if c1:
            return -c1
        return cmp(chr1, chr2)

    ordered = sorted(entropydict.iteritems(), cmp=cmpchrent)
    ladder = [0]
    lchars = []
    char2i = {}
    lookup = []
    for i, (chr, ent) in enumerate(ordered):
        char2i[chr] = i
        lchars.append(chr)
        ladder.append(ladder[i] + ent)
        lookup.extend([i] * ent)
    return ladder, lchars, char2i, lookup

def main():
    text = """\
    This work is addressed to two classes of readers. From both of these alike\
 the translator begs sympathy and co-operation. The Anglo-Saxon scholar he\
 hopes to please by adhering faithfully to the original. The student of\
 English literature he aims to interest by giving him, in modern garb, the\
 most ancient epic of our race. This is a bold and venturesome undertaking;\
 and yet there must be some students of the Teutonic past willing to follow\
 even a daring guide, if they may read in modern phrases of the sorrows of\
 Hrothgar, of the prowess of Beowulf, and of the feelings that stirred the\
 hearts of our forefathers in their primeval homes."""

    text = "ABCCCCDDDDDDDeeeeeeeeeeeee"* 10

    cntarr = [0] * 256
    for c in text:
        cntarr[ord(c)] += 1
    cntdict = {}
    for i, c in enumerate(cntarr):
        if not c:
            continue
        cntdict[chr(i)] = c

    entdict = entropy(cntdict)
    ladder, lchars, char2i, lookup = entropy2tables(entdict)

    # encode
    buffer = StrStream("")
    encoder = REncoder(buffer)
    for c in text:
        i = char2i[c]
        encoder.enc(ladder[i], ladder[i + 1] - ladder[i])
    encoder.flush()
    encoded = buffer.getStr()[1:]
    print "encoded len:", len(encoded)
    # decode
    buffer = StrStream(encoded)
    decoder = RDecoder(buffer)
    deced = []
    for _t in range(len(text)):
        mid = decoder.mid()
        i = lookup[mid]

        if lchars[i] != text[len(deced)]:
            print "error:", i, lchars[i], buffer.getI()

        deced.append(lchars[i])

        decoder.dec(ladder[i], ladder[i + 1] - ladder[i])

    outtext = ''.join(deced)
    print "i:", buffer.getI()
    print len(text)
    print outtext
    print text
    assert outtext == text


if __name__ == '__main__':
    main()
