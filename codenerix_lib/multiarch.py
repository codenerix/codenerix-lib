#! /usr/bin/env python3
import subprocess

from codenerix_lib.debugger import Debugger


def whatismyarch():
    # whatismyarch = (
    #     """echo "`gcc -### -E - -march=native 2>&1 """
    #     """| sed -r '/cc1/!d;s/(")|(^.* - )//g' | sed -r 's# #\n#g' """
    #     '''| grep march | cut -d "=" -f 2 || echo "Unknown"`"'''
    # )

    # Get info from gcc
    output = subprocess.check_output(
        ["gcc", "-###", "-E", "-", "-march=native"],
        stderr=subprocess.STDOUT,
    ).decode()

    # Find march
    march = output.find('"-march=')
    if march > 0:
        arch = output[march + len('"-march=') :].split('"')[0]
    else:
        arch = None  # pragma: no cover

    return arch


def multiarch_import(name, sufix=None, using=False):
    """
    Dynamic import for multiarch libraries to match
    the machine architecture
    """

    # Initialize debugger
    d = Debugger()
    d.set_debug()
    d.set_name("Multiarch")

    # Detecte if sufix was given
    imported = None
    if sufix:
        # Use it as expected
        try:
            imported = __import__("{}{}".format(name, sufix))
            if using:  # pragma: no cover
                d.debug("Using {}{}".format(name, sufix), color="cyan")
        except Exception:
            d.warning(
                f"I have tried to import the library '{name}' as you "
                f"requested using sufix '{sufix}' but I have failed to "
                f"import {name}{sufix}, maybe you have forgotten to install "
                "the python library, I will try to import the default "
                "library!",
            )

    elif sufix != "":
        # No sufix was given, try to detect the architecture
        # using 'whatismyarch()'
        try:
            arch = whatismyarch()
        except Exception as e:
            arch = None
            d.warning(
                "I have tried to guess your machine architecture "
                "using 'whatismyarch()', but the command has failed, do you "
                "have gcc command installed?, I will try to import the "
                f"default library! (Error was: {e})",
            )

        # We got an architecture
        if arch:
            # Try to import detected architecture
            try:
                imported = __import__(f"{name}_{arch}")
                if using:  # pragma: no cover
                    d.debug(f"Using {name}_{arch}", color="cyan")
            except Exception:
                d.warning(
                    "I have guessed with 'whatismyarch()' that your "
                    f"architecture is '{arch}', but I have failed to "
                    f"import {name}_{arch}, maybe you have forgotten "
                    "to install the python library for your architecture, "
                    "I will try to import the default library!",
                )
        else:
            d.warning(
                "I couldn't find your architecture with 'whatismyarch()', "
                "it will try to import the default library!",
            )

    if not imported:
        # No architecture detected, try to import the base library!
        try:
            imported = __import__(name)
            if using:  # pragma: no cover
                d.debug(f"Using {name}", color="cyan")
        except Exception:
            d.debug(
                f"Error while import {name}, maybe you have forgotten "
                "to install the python base library or your environment "
                "doesn't have it installed. This script is not able to "
                "find it!",
                color="red",
            )
            raise

    return imported
