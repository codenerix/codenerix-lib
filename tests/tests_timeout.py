import time

from pytest import raises

from codenerix_lib.timeout import TimedOutException, timeout, timeout2


def slow(num):
    for i in range(num):
        time.sleep(0.1)


def test_timeout():
    with raises(IOError):
        timeout(slow, 0, 5)

    with raises(IOError):
        timeout(slow, -1, 5)

    # Fast
    timeout(slow, 1, 5)

    # Slow
    with raises(TimedOutException) as error:
        timeout(slow, 1, 15)
    assert str(error.value) == "Timed Out"


def test_timeout2():
    # Basic control
    with raises(IOError):
        timeout2(slow, 0, None, 0.1, [5])
    with raises(IOError):
        timeout2(slow, -1, None, 0.1, [5])

    # Fast
    timeout2(slow, 1, None, 0.1, [5])

    # Slow
    with raises(TimedOutException):
        timeout2(slow, 1, None, 0.1, [15])
