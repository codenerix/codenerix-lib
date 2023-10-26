import sys
from datetime import datetime

from codenerix_lib.debugger import Debugger, lineno


def test_debugger(capsys, mocker):
    # Mock datetime
    now = datetime(2020, 12, 31, 12, 13, 14)
    mock_datetime = mocker.MagicMock(wraps=datetime)
    mock_datetime.now.return_value = now
    mocker.patch("codenerix_lib.debugger.datetime", mock_datetime)

    # Prepare debugger
    debugger = Debugger()
    debugger.set_debug()
    assert debugger.get_debug() == {"screen": (sys.stdout, ["*"])}

    # Check wrong collor
    debugger.color("ABC")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "31/12/2020 12:13:14 Debugger        - \x1b[1;31mColor 'ABC' unknown\x1b[1;00m\n\x1b[1;00m\n"  # noqa: E501
    )

    # Check naming
    assert debugger.get_name() is None
    debugger.set_name("TEST")
    assert debugger.get_name() == "TEST"

    # Normal debug
    debugger.debug("Hola")
    cap = capsys.readouterr()
    assert cap.out == "31/12/2020 12:13:14 TEST            - Hola\x1b[1;00m\n"

    # No head
    debugger.debug("Hola", header=False)
    cap = capsys.readouterr()
    assert cap.out == "Hola\x1b[1;00m\n"

    # No head
    debugger.debug("Hola", head=False)
    cap = capsys.readouterr()
    assert cap.out == "Hola\x1b[1;00m\n"

    # No tail
    debugger.debug("Hola", tail=False)
    cap = capsys.readouterr()
    assert cap.out == "31/12/2020 12:13:14 TEST            - Hola\x1b[1;00m"

    # No tail
    debugger.debug("Hola", footer=False)
    cap = capsys.readouterr()
    assert cap.out == "31/12/2020 12:13:14 TEST            - Hola\x1b[1;00m"

    # Check mix
    debugger.debug("Hola", head=False, tail=False)
    debugger.debug("caracola", head=False)
    cap = capsys.readouterr()
    assert cap.out == "Hola\x1b[1;00mcaracola\x1b[1;00m\n"

    # Blue color
    debugger.debug("Hola", color="blue")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "\x1b[1;34m31/12/2020 12:13:14 TEST            - Hola\x1b[1;00m\n"
    )

    # Primary
    debugger.primary("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "\x1b[1;34m\nPRIMARY - 31/12/2020 12:13:14 TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Secondary
    debugger.secondary("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "\x1b[1;35m\nSECONDARY - 31/12/2020 12:13:14 TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Success
    debugger.success("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "\x1b[1;32m\nSUCCESS - 31/12/2020 12:13:14 TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Danger
    debugger.danger("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out
        == "\x1b[0;31m\nDANGER - 31/12/2020 12:13:14 TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Warning
    line = lineno() + 1
    debugger.warning("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out == "\x1b[1;33m\nWARNING - 31/12/2020 12:13:14 "
        f"tests/tests_debugger_debug.py:{line}: TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Info
    debugger.info("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out == "\x1b[1;36m\nINFO - 31/12/2020 12:13:14 TEST            - "
        "Hola\x1b[1;00m\n"
    )

    # Error
    line = lineno() + 1
    debugger.error("Hola")
    cap = capsys.readouterr()
    assert (
        cap.out == "\x1b[1;31m\nERROR - 31/12/2020 12:13:14 "
        f"tests/tests_debugger_debug.py:{line}: TEST            - "
        "Hola\x1b[1;00m\n"
    )
