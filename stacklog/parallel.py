from contextlib import contextmanager
"""

maybe the default behavior is to pop the stack to a list for holding
....and then later call a collection function?

"""
dv = None

"""
maybe the data structure we really want is
key: [(value, children),(value, children),(value, children)]

where each value is the time it took on each process.

'prox': [(total_time, {}), ]

"""

# put the wrapping timing code in runner?

def runner():
    import stacklog
    return stacklog.gather()

@contextmanager
def par(key):
    global logs, dv
    logger = logs['default']

    # clear the remote stacks
    dv.execute('stacklog.gather()', block=True)

    logger.tic(key)
    yield
    elapsed, children = logger.toc(record=False)

    dicts = dv.apply_sync(runner)
    logger.record(key, elapsed, children, *dicts)


def paralell_init(the_dv):
    global dv
    dv = the_dv

    #todo: relative import?
    dv.execute('import stacklog', block=True)
