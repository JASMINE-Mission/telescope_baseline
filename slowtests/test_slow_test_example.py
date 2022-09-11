import pytest
import time
from test_tools.assert_timeout import assert_timeout


def test_slow():
    # assert_timeout(10 * 1000, lambda: time.sleep(5))  # not error
    assert_timeout(4 * 1000, lambda: time.sleep(5))    # error
