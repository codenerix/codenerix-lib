import os
import tempfile

from pytest import raises

from codenerix_lib.pylock import AlreadyLocked, PyLock


def test_pylock():
    # Get temporal file
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()

    # Get temporal filename
    filename = tempfile.mktemp()
    assert not os.path.exists(filename)
    locker0 = PyLock(filename, "lock")
    assert os.path.exists(filename)
    locker0.lock()
    del locker0
    os.unlink(filename)
    assert not os.path.exists(filename)

    # Wrong type
    with raises(TypeError) as error:
        locker1 = PyLock(f.name, "abc")
    assert str(error.value) == "Locking type unknown"

    # locker1 = PyLock(f.name, "lock", verbose="1")
    # locker2 = PyLock(f.name, "lock", verbose="2")
    locker1 = PyLock(f.name, "lock")
    locker2 = PyLock(f.name, "lock")

    locker1.lock()
    with raises(AlreadyLocked) as error:
        locker2.lock()
    locker1.free()
    assert str(error.value) == "File is already locked"

    locker2.lock()
    with raises(AlreadyLocked) as error:
        locker1.lock()
    locker2.free()
    assert str(error.value) == "File is already locked"

    # Remove the temporal file
    os.unlink(f.name)
