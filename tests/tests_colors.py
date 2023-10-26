from codenerix_lib.colors import colorize, get_colors


def test_colors():
    expected = (
        "0:30 - \x1b[0;30msimplegrey    \x1b[1;00msimplegrey\n"
        "0:31 - \x1b[0;31msimplered     \x1b[1;00msimplered\n"
        "0:32 - \x1b[0;32msimplegreen   \x1b[1;00msimplegreen\n"
        "0:33 - \x1b[0;33msimpleyellow  \x1b[1;00msimpleyellow\n"
        "0:34 - \x1b[0;34msimpleblue    \x1b[1;00msimpleblue\n"
        "0:35 - \x1b[0;35msimplepurple  \x1b[1;00msimplepurple\n"
        "0:36 - \x1b[0;36msimplecyan    \x1b[1;00msimplecyan\n"
        "0:37 - \x1b[0;37msimplewhite   \x1b[1;00msimplewhite\n"
        "1:00 - \x1b[1;00mclose         \x1b[1;00mclose\n"
        "1:30 - \x1b[1;30mgrey          \x1b[1;00mgrey\n"
        "1:31 - \x1b[1;31mred           \x1b[1;00mred\n"
        "1:32 - \x1b[1;32mgreen         \x1b[1;00mgreen\n"
        "1:33 - \x1b[1;33myellow        \x1b[1;00myellow\n"
        "1:34 - \x1b[1;34mblue          \x1b[1;00mblue\n"
        "1:35 - \x1b[1;35mpurple        \x1b[1;00mpurple\n"
        "1:36 - \x1b[1;36mcyan          \x1b[1;00mcyan\n"
        "1:37 - \x1b[1;37mwhite         \x1b[1;00mwhite"
    )

    assert get_colors() == expected


def test_colorize():
    assert colorize("ABC", "red") == "\x1b[1;31mABC\x1b[1;00m"
    assert colorize("ABC", "simplered") == "\x1b[0;31mABC\x1b[1;00m"
    assert colorize("ABC", "abc") == "\x1b[1;00mABC\x1b[1;00m"
