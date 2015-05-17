# stacklog
Nested benchmarking and timing for Python code.

Read the [tutorial on GitHub](docs/tutorial.ipynb) or [on nbviewer](http://nbviewer.ipython.org/github/ajfriend/stacklog/blob/master/docs/tutorial.ipynb).

## Install
`pip install https://github.com/ajfriend/stacklog.git`


## Example
`tic`, `toc`, and `timer` can be used to time sections of code. The Python snippet
```python
from stacklog import tic, toc, timer, pull, pretty_dict
import time

def comp(t=.1):
    time.sleep(t)

tic('first')
for i in range(4):
    with timer('loop'):
        comp(.5)
toc()

with timer('outside'):
    comp(1.2)

pretty_dict(pull())
```

has output

```python
{'first': (2.004528045654297,
           {'loop': [0.5031731128692627,
                     0.5004160404205322,
                     0.5002670288085938,
                     0.50016188621521]}),
 'outside': 1.2026138305664062}
```
