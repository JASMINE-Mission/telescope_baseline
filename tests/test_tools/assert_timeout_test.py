import pytest
import time
from test_tools.assert_timeout import assert_timeout


def test_assert_timeout__return_value():
    func = lambda: 3
    ret = assert_timeout(1000, func)
    assert ret == 3


def dummy_func():
    pass

def test_assert_timeout__void_func():
    func = dummy_func
    ret = assert_timeout(1000, func)
    assert ret == None


def test_assert_timeout__timeout():
    func = lambda : time.sleep(1.1)
    try:
        assert_timeout(1000, func)
        print('タイムアウトせず')
    except AssertionError:
        print('タイムアウトした!!')
        return
    assert 1 == 2, "タイムアウトしていません"

