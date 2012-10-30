from coldb.pyrange import countstr, entropy, entropy2tables
from coldb.pyrange import range_encode, range_decode

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
 
    
    cntdict = countstr(text)
    entropydict = entropy(cntdict)
    ladder, lchars, char2i, lookup = entropy2tables(entropydict)
    result = range_encode(text, ladder, lchars, char2i, lookup)
    orglen = len(text)
    clen = len(result)
    print "before: %d" % orglen
    print "after: %d" % clen
    print "compress ratio: %f" % (float(clen) / float(orglen))

if __name__ == '__main__':
    main()
