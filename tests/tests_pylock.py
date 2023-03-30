import os
import tempfile

from pytest import fixture
from pytest import raises

from codenerix_lib.pylock import AlreadyLocked
from codenerix_lib.pylock import PyLock


@fixture
def verbose():
    return False


def test_pylock(verbose):
    # Get temporal file
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()

    if verbose:
        locker1 = PyLock(f.name, "lock", verbose="1")
        locker2 = PyLock(f.name, "lock", verbose="2")
    else:
        locker1 = PyLock(f.name, "lock")
        locker2 = PyLock(f.name, "lock")

    locker1.lock()
    with raises(AlreadyLocked):
        locker2.lock()
    locker1.free()

    locker2.lock()
    with raises(AlreadyLocked):
        locker1.lock()
    locker2.free()

    # Remove the temporal file
    os.unlink(f.name)
