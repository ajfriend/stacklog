from contextlib import contextmanager
import time
from .util import pretty_log

# what's the data format? optional children? optional parallel shit?

# todo: make it so you can use different timers?


class Logger(object):
    r""" A stack (list) of dictionaries.
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
        # the top of the stack is always a dictionary, which is waiting to capture new input
        self.stack = [{}]

    def reset(self):
        self.stack = [{}]

    def tic(self, key):
        # start the timer, with a given key and the current time
        # we push a *tuple* onto the stack to do this
        self.stack.append((key, time.time()))
        # add a dictionary to the stack to capture any subordinate information
        self.stack.append({})

    def toc(self, record=True):
        # we stop the timer
        end = time.time()
        # pop any subordinate info from the stack
        children = self.stack.pop()
        # pop off the tuple pushed on by the matching `tic`
        key, start = self.stack.pop()

        elapsed = end-start

        if record:
            self.record(key, elapsed, children)

        # return the elapsed time and any subordinate info
        return elapsed, children

    @contextmanager
    def timer(self, key):
        # if once and len(self.stack[-1].setdefault(key, [])) > 0:
        #     raise Exception('Expecting to time this only once in the current context!')
        self.tic(key)
        yield
        self.toc()

    def gather(self):
        """ To be used only at the top most level, not in the middle of any timings.

        Returns the nested dictionary of logs and resets the stack to be empty.
        """
        result = self.peek()
        self.reset()
        return result

    def peek(self):
        """ To be used only at the top most level, not in the middle of any timings.

        Returns the nested dictionary of logs without resetting the stack.
        """
        if len(self.stack) != 1:
            raise Exception('The stack should have exactly one dictionary on it.')
        return self.stack[0]

    def record(self, key, value, *children):
        """ Push key: (value, children) into the *top* dictionary of the stack
        """
        self.stack[-1].setdefault(key, []).append((value,) + children)

    def record_root(self, key, value, *children):
        """ Push key: (value, children) into the *bottom* dictionary of the stack
        """
        self.stack[0].setdefault(key, []).append((value,) + children)

    def __repr__(self):
        return pretty_log(self)

    def __str__(self):
        return repr(self)


