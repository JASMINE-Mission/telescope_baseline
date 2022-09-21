import time


def assert_timeout(timeout_milliseconds: int, func):
    """Measure the time for a specific process and send an AssertionError if it exceeds the threshold value.

    Args:
        timeout_milliseconds:Timeout threshold(milli seconds)
        func:Measured Processing

    Returns:
        Return value of func. If there is no return value, return None.

    Exaples:

        >>> from test_tools.assert_timeout import assert_timeout
        >>> func = lambda : time.sleep(1.1)
        >>> assert_timeout(2000, func)  # not thrown AssertionError
        >>> assert_timeout(1000, func)  # thrown AssertionError

    """
    start = time.time() * 1000
    ret = func()
    end = time.time() * 1000
    period = end - start
    if period > timeout_milliseconds:
        raise AssertionError('timeout:limit:[%d]ms actual:[%d]ms' % (timeout_milliseconds, period))
    return ret
