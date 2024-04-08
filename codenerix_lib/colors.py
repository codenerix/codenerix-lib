#!/usr/bin/env python3
#
# django-codenerix
#
# Codenerix GNU
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Colors definition
"""
from colorama import init

init()

__version__ = "201109111106"


__all__ = ["colors"]


# Colors
colors = {
    # Simple
    "simplegrey": (0, 30),
    "simplered": (0, 31),
    "simplegreen": (0, 32),
    "simpleyellow": (0, 33),
    "simpleblue": (0, 34),
    "simplepurple": (0, 35),
    "simplecyan": (0, 36),
    "simplewhite": (0, 37),
    # Bold
    "grey": (1, 30),
    "red": (1, 31),
    "green": (1, 32),
    "yellow": (1, 33),
    "blue": (1, 34),
    "purple": (1, 35),
    "cyan": (1, 36),
    "white": (1, 37),
    # Close
    "close": (1, 0),
}

# HTML Colors
html_colors = {
    # Simple
    "simplegrey": (0, (128, 128, 128)),
    "simplered": (0, (255, 0, 0)),
    "simplegreen": (0, (0, 255, 0)),
    "simpleyellow": (0, (255, 255, 0)),
    "simpleblue": (0, (0, 0, 255)),
    "simplepurple": (0, (128, 0, 128)),
    "simplecyan": (0, (0, 255, 255)),
    "simplewhite": (0, (255, 255, 255)),
    # Bold
    "grey": (1, (169, 169, 169)),
    "red": (1, (255, 69, 0)),
    "green": (1, (0, 128, 0)),
    "yellow": (1, (255, 255, 0)),
    "blue": (1, (0, 0, 255)),
    "purple": (1, (128, 0, 128)),
    "cyan": (1, (0, 255, 255)),
    "white": (1, (255, 255, 255)),
}


def colorize(msg, color=None):
    # Colors
    if color in colors:
        (darkbit, subcolor) = colors[color]
    else:
        (darkbit, subcolor) = (1, 0)

    # Prepare the message
    result = "\033[%1d;%02dm" % (darkbit, subcolor)
    result += msg
    result += "\033[%1d;%02dm" % (1, 0)

    # Return the result
    return result


def get_colors():
    # Reorder colors
    keys = []
    for key in colors.keys():
        keys.append((colors[key][0], colors[key][1], key))
    keys.sort()

    # Show up all colors
    buffer = ""
    for color in keys:
        # Get the color information
        (simplebit, subcolor) = colors[color[2]]
        if len(buffer) > 0:
            buffer += "\n"
        # Show it
        buffer += (
            f"{simplebit:1d}:{subcolor:02d} - "
            f"\033[{simplebit:1d};{subcolor:02d}m{color[2]:<14s}"
            f"\033[1;00m{color[2]:<s}"
        )
    return buffer


if __name__ == "__main__":  # pragma: no cover
    print(get_colors())
