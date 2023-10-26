from codenerix_lib.debugger import __FILE__, __LINE__, lineno


def test_lineno():
    assert lineno() == 5


def test___line__():
    assert __LINE__() == 9


def test___file__():
    assert __FILE__() == "tests/tests_debugger_base.py"
