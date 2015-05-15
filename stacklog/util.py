from pprint import pformat


def pretty_log(log, depth=None, clean=True):
    s = []
    for i, item in enumerate(log.stack):
        s.append('Stack item {}:\n'.format(i))
        if isinstance(item, dict):
            s.append(pretty_dict(item, depth, clean))

        elif isinstance(item, tuple):
            s.append(str(item))
        else:
            raise ValueError('We expect the stack log to include only tuples and dictionaries.')

    return '\n'.join(s)


def pretty_dict(d, depth=None, clean=True):
    if clean:
        d = clean_dict(d)
    return pformat(d, depth=depth)


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


def time_sum(d):
    pass
    # write the function to do this for a single tuple
    # check that every thing's children sum to somthin less than the elapsed valuep


# maybe add a function that computes variance over the experiment?

# maybe make a dict that shows the gap in every value and its children (if it has children)
# make an equivalent one for max (parallel)

# be able to print out the stack log even when it isn't cleared
# this would be good to see where it is, and debug
