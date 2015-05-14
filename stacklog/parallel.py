from contextlib import contextmanager
"""

maybe the default behavior is to pop the stack to a list for holding
....and then later call a collection function?

"""

def runner():
    import stacklog
    return stacklog.pull()

@contextmanager
def par(key):
    global logs, dv
    logger = logs['default']

    # clear the remote stacks
    dv.execute('stacklog.pull()', block=True)

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