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
