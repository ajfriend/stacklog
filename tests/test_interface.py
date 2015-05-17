import time
import stacklog as sl
from contextlib import contextmanager

@contextmanager
def cond_manager(on=True):
    if on:
        with sl.timer('previously unaccounted for'):
            yield
    else:
        yield


def comp(t=.1):
    time.sleep(t)


def run_timing(manager_on=True):

    with sl.timer('outer'):
        sl.tic('inner')
        comp()
        sl.toc()

        with sl.timer('another inner'):
            with cond_manager(manager_on):
                comp()
                comp()
                comp()
            for i in range(4):
                with sl.timer('way in there'):
                    comp()


def test_interface():

    # the 3 inner `comp()`s are timed or not
    for cover in False, True:
        sl.reset()
        run_timing(cover)

        result = sl.lost_time(sl.peek())

        assert result['outer'][0][0] >= 0
        assert result['outer'][0][1]['another inner'][0][0] >= 0
        assert result['outer'][0][0] <= 0.05

        if cover:
            # unaccounted for time should be small
            assert result['outer'][0][1]['another inner'][0][0] <= 0.05
        else:
            # unaccounted for time should be about the time to execute `comp()` 3 times
            assert 0.3 <= result['outer'][0][1]['another inner'][0][0] <= 0.35


def test_pretty_print():
    sl.reset()
    run_timing()
    print('Outputs:')
    sl.pretty_dict(sl.peek())
    sl.pretty_log(sl.log())







