import pprint


def pretty(d, depth=None, clean=True):
    if clean:
        d = clean_dict(d)
    pprint.pprint(d, depth=depth)


def clean_tuple(t):
    value, children = t[0], t[1:]
    if any(len(c) > 0 for c in children):
        return (value,) + tuple(clean_dict(c) for c in children)
    else:
        return value


def clean_dict(d):
    result = {}
    for k, l in d.iteritems():
        if len(l) == 1:
            result[k] = clean_tuple(l[0])
        else:
            result[k] = [clean_tuple(t) for t in l]

    return result
