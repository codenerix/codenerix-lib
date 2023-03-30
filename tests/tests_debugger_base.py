from codenerix_lib.debugger import __FILE__
from codenerix_lib.debugger import __LINE__
from codenerix_lib.debugger import lineno


def test_lineno():
    assert lineno() == 7


def test___line__():
    assert __LINE__() == 11


def test___file__():
    assert __FILE__() == "tests/tests_debugger_base.py"
