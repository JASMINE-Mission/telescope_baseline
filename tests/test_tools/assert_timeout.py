import time


def assert_timeout(timeout_milliseconds: int, func):
    start = time.time() * 1000
    ret = func()
    end = time.time() * 1000
    period = end - start
    if period > timeout_milliseconds:
        raise AssertionError('timeout:limit:[%d]ms actual:[%d]ms' % (timeout_milliseconds, period))
    return ret
