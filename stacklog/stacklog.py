from contextlib import contextmanager
import time

dv = None
active = True  # to turn on and off logging


class Logger(object):
    """ A stack (list) of dictionaries.
        Each item in dict is of the form
        key: [(value, *children),...]
        where *children is a list of 0 or more dictionarires, denoting subordinate timers.
        The first is any local subordinate timers. any further timers denote ones
        run on parallel machines and then collected later

        with log.paralell():
            #do the map reduce
        finally:
            collect all the stuff and include
    """

    def __init__(self):
        self.stack = [{}]

    def reset(self):
        self.stack = [{}]

    def peek(self):
        if len(self.stack) != 1:
            raise Exception('The stack should have exactly one dictionary on it.')
        return self.stack[0]

    def pull(self):
        result = self.peek()
        self.stack = [{}]
        return result

    @contextmanager
    def timer(self, key, once=False):
        if once and len(self.stack[-1].setdefault(key, [])) > 0:
            raise Exception('Expecting to time this only once in the current context!')

        self.tic(key)
        yield
        self.toc()

    def record_root(self, key, value, *children):
        self.stack[0].setdefault(key, []).append((value,) + children)

    def record(self, key, value, *children):
        self.stack[-1].setdefault(key, []).append((value,) + children)

    def tic(self, key):
        self.stack.append((key, time.time()))
        self.stack.append({})

    def toc(self, record=True):
        end = time.time()
        children = self.stack.pop()
        key, start = self.stack.pop()
        elapsed = end-start

        if record:
            self.record(key, elapsed, children)
        return elapsed, children


# dictionary of loggers
logs = {'default': Logger()}

