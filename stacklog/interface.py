# code for the module interface
from contextlib import contextmanager

## module API
@contextmanager
def timer(key, once=False):
    global logs
    logger = logs['default']
    # context manager inside a context manager!
    with logger.timer(key, once):
        yield

def record_root(key, value, *children):
    global logs
    logger = logs['default']
    logger.record_root(key, value, *children)

def record(key, value, *children):
    global logs
    logger = logs['default']
    logger.record(key, value, *children)

def reset():
    global logs
    logger = logs['default']
    logger.reset()

def tic(key):
    global logs
    logger = logs['default']
    logger.tic(key)

def toc(record=True):
    global logs
    logger = logs['default']
    return logger.toc(record=record)

def peek():
    global logs
    logger = logs['default']
    return logger.peek()

def pull():
    global logs
    logger = logs['default']
    return logger.pull()
