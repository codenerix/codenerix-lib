import os
from datetime import datetime

from pytest import raises

from codenerix_lib.multiarch import multiarch_import, whatismyarch


def test_whatismyarch():
    arch = whatismyarch()
    assert arch is None or isinstance(arch, str)


def test_multiarch_no_whatismyarch(capsys, mocker):
    mocker.patch("codenerix_lib.multiarch.whatismyarch", return_value=None)
    # Import OS With no sufix
    multiarch_import("os")
    cap = capsys.readouterr()
    assert (
        "I couldn't find your architecture with 'whatismyarch()', it will try "
        "to import the default library!" in cap.out
    )


def test_multiarch_error_whatismyarch_sufix(capsys, mocker):
    mocker.patch(
        "codenerix_lib.multiarch.whatismyarch",
        side_effect=Exception(),
    )
    # Import OS With no sufix
    multiarch_import("os", "abc")
    cap = capsys.readouterr()
    assert (
        "I have tried to import the library 'os' as you requested using "
        "sufix 'abc' but I have failed to import osabc, maybe you have "
        "forgotten to install the python library, I will try to import "
        "the default library!" in cap.out
    )


def test_multiarch_error_whatismyarch_nosufix(capsys, mocker):
    mocker.patch(
        "codenerix_lib.multiarch.whatismyarch",
        side_effect=Exception("ABC"),
    )
    # Import OS With no sufix
    multiarch_import("os")
    cap = capsys.readouterr()
    assert (
        "I have tried to guess your machine architecture using "
        "'whatismyarch()', but the command has failed, do you have gcc "
        "command installed?, I will try to import the default library! "
        "(Error was: ABC)" in cap.out
    )
    assert (
        "I couldn't find your architecture with 'whatismyarch()', it will "
        "try to import the default library!" in cap.out
    )


def test_multiarch_import(capsys, mocker):
    # Mock datetime
    now = datetime(2020, 12, 31, 12, 13, 14)
    mock_datetime = mocker.MagicMock(wraps=datetime)
    mock_datetime.now.return_value = now
    mocker.patch("codenerix_lib.debugger.datetime", mock_datetime)

    # Mock whatismyarch
    mock_whatismyarch = mocker.patch("codenerix_lib.multiarch.whatismyarch")
    mock_whatismyarch.return_value = "alderlake"

    # Import OS with default sufix
    imported = multiarch_import("os")
    cap = capsys.readouterr()
    outsp = cap.out.split(" ")
    outsp[4] = "<FILE>:"
    assert imported is os
    assert (
        " ".join(outsp)
        == "\x1b[1;33m\nWARNING - 31/12/2020 12:13:14 <FILE>: Multiarch       - I have guessed with 'whatismyarch()' that your architecture is 'alderlake', but I have failed to import os_alderlake, maybe you have forgotten to install the python library for your architecture, I will try to import the default library!\x1b[1;00m\n"  # noqa: E501
    )

    # Import OS with no sufix
    imported = multiarch_import("os", "")
    cap = capsys.readouterr()
    assert imported is os
    assert cap.out == ""

    # Import OS with specific sufix
    imported = multiarch_import("os", "abc")
    cap = capsys.readouterr()
    outsp = cap.out.split(" ")
    outsp[4] = "<FILE>:"
    assert imported is os
    assert (
        " ".join(outsp)
        == "\x1b[1;33m\nWARNING - 31/12/2020 12:13:14 <FILE>: Multiarch       - I have tried to import the library 'os' as you requested using sufix 'abc' but I have failed to import osabc, maybe you have forgotten to install the python library, I will try to import the default library!\x1b[1;00m\n"  # noqa: E501
    )

    # Import abc123abc123
    imported = None
    with raises(ModuleNotFoundError):
        imported = multiarch_import("abc123abc123", "abc")
    cap = capsys.readouterr()
    outsp = cap.out.split(" ")
    outsp[4] = "<FILE>:"
    assert imported is None
    assert (
        " ".join(outsp)
        == "\x1b[1;33m\nWARNING - 31/12/2020 12:13:14 <FILE>: Multiarch       - I have tried to import the library 'abc123abc123' as you requested using sufix 'abc' but I have failed to import abc123abc123abc, maybe you have forgotten to install the python library, I will try to import the default library!\x1b[1;00m\n\x1b[1;31m31/12/2020 12:13:14 Multiarch       - Error while import abc123abc123, maybe you have forgotten to install the python base library or your environment doesn't have it installed. This script is not able to find it!\x1b[1;00m\n"  # noqa: E501
    )
