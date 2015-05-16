from pprint import pformat

__all__ = ['pretty_log', 'pretty_dict', 'lost_time']


# def pretty(data, depth=None, clean=True, show=True):
#
#     if isinstance(data, Logger):
#         s = pretty_log(data, depth, clean)
#     elif isinstance(data, dict):
#         s = pretty_dict(data, depth, clean)
#     else:
#         raise ValueError('Expecting to pretty print a Logger or tuple.')
#
#     if show:
#         print(s)
#     else:
#         return s


def pretty_log(log, depth=None, clean=True, show=True):
    s = []
    for i, item in enumerate(log.stack):
        s.append('Stack item {}:\n'.format(i))
        if isinstance(item, dict):
            s.append(pretty_dict(item, depth, clean, show=False))

        elif isinstance(item, tuple):
            s.append(str(item))
        else:
            raise ValueError('We expect the stack log to include only tuples and dictionaries.')

    s = '\n'.join(s)
    if show:
        print(s)
    else:
        return s


def pretty_dict(d, depth=None, clean=True, show=True):
    if clean:
        d = clean_dict(d)
    s = pformat(d, depth=depth)
    if show:
        print(s)
    else:
        return s




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


def dictlistmap(func, d):
    d2 = {}
    for key in d:
        val = [func(item) for item in d[key]]
        if not all(item is None for item in val):
            d2[key] = val
    return d2


def lost_time(d):
    return dictlistmap(time_diff_tup, d)


def time_diff_tup(t):
    """ For a single tuple, return the difference in the recorded
        total time and the sum of the subordinate times.

        Return the same for the children dicts.
    """
    dicts = t[1:]
    if dicts[0]:
        total = 0.0
        for l in dicts[0].values():
            for tup in l:
                total += tup[0]

        return t[0] - total, lost_time(dicts[0])


# maybe add a function that computes variance over the experiment?

# maybe make a dict that shows the gap in every value and its children (if it has children)
# make an equivalent one for max (parallel)
