import pytest
import time
from test_tools.assert_timeout import assert_timeout


def test_slow():
    slow_func = lambda: time.sleep(5)
    assert_timeout(10 * 1000, slow_func)    # not error
    #assert_timeout(4 * 1000, slow_func)    # error
