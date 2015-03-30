
from contextlib import contextmanager
import time
import pprint

dv = None
active = True  # to turn on and off logging

#split serial and paralell into two files?

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

def paralell_init(the_dv):
    global dv
    dv = the_dv

    #todo: relative import?
    dv.execute('import stacklog', block=True)

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