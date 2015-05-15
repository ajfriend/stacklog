# code for the module interface
from contextlib import contextmanager
from .stacklog import Logger
from collections import defaultdict

# dictionary of loggers
logs = defaultdict(Logger)
logs['default'] = Logger()
#active = True  # to turn on and off logging


# log(name).timer()
def log(name='default'):
    global logs
    return logs[name]


@contextmanager
def timer(key):
    # context manager inside a context manager!
    with log().timer(key):
        yield


def record_root(key, value, *children):
    log().record_root(key, value, *children)


def record(key, value, *children):
    log().record(key, value, *children)


def reset():
    log().reset()


def tic(key):
    log().tic(key)


def toc(record=True):
    return log().toc(record=record)


def peek():
    return log().peek()


def gather():
    return log().gather()
