# -*- coding: utf-8 -*-
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
Library to handle lockers over files
"""

__version__ = "2015061200"

import os
import fcntl
import unittest
import tempfile

__all__ = ["pylock", "AlreadyLocked"]


class pylock:
    """
    Function to control locking flags over a file
    """

    def __init__(self, lockfile, locktype, verbose=False):
        """
        Parameters:
        - `lockfile`: name of the file to check/apply the locking.
        - `locktype`: possible values are:
                wait: on a call to lock() function, the system will wait to get the locker
                lock: on a call to lock() function, if locked the system will raise an AlreadyLocked exception
        - `verbose`:  enable verbose mode
        """

        # Save config
        self.__lockfile = lockfile
        self.__locktype = locktype
        self.__fd = None
        self.__verbose = verbose

        # Show header if verbose
        if self.__verbose:
            print(
                '{} - VERBOSE MODE ENABLED: lockfile="{}" - locktype="{}"'.format(
                    self.__verbose, self.__lockfile, self.__locktype
                )
            )

        # Check file exists and create it if it does not
        if not os.path.exists(lockfile):
            if self.__verbose:
                print(
                    "{} - Lockfile not found, creating a new one!".format(
                        self.__verbose
                    )
                )
            file = open(lockfile, "w")
            file.close()

        # Check locktype
        if locktype not in ["wait", "lock"]:
            raise TypeError("Locking type unkown")

    def __del__(self):
        """
        when dying make sure the lock become free
        """
        # If file was open, close it and delete it!
        if self.__fd:
            if self.__verbose:
                print("{} - Cloing FD".format(self.__verbose))
            self.__fd.close()
            self.__fd = None

    def lock(self):
        """
        Try to get locked the file
        - the function will wait until the file is unlocked if 'wait' was defined as locktype
        - the funciton will raise AlreadyLocked exception if 'lock' was defined as locktype
        """

        # Open file
        if not self.__fd:
            if self.__verbose:
                print("{} - Opening FD".format(self.__verbose))
            self.__fd = open(self.__lockfile, "wb")

        if self.__locktype == "wait":
            # Try to get it locked until ready
            if self.__verbose:
                print("{} - Wait lock!".format(self.__verbose))
            fcntl.flock(self.__fd.fileno(), fcntl.LOCK_EX)
        elif self.__locktype == "lock":
            # Try to get the locker if can not raise an exception
            if self.__verbose:
                print("{} - Normal lock!".format(self.__verbose))
            try:
                fcntl.flock(self.__fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                if self.__verbose:
                    print("{} - Already locked!".format(self.__verbose))
                raise AlreadyLocked("File is already locked")

    def free(self):
        """
        Set the locked file free
        """

        if self.__verbose:
            print("{} - Free lock! (Closing FD)".format(self.__verbose))

        # Close file
        self.__fd.close()
        self.__fd = None


# Exceptions classes
class AlreadyLocked(Exception):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string


# Testing
class test_pylock(unittest.TestCase):
    """
    Testing class for pylock
    """

    verbose = False

    def setUp(self):
        pass

    def testpylock(self):
        # Get temporal file
        f = tempfile.NamedTemporaryFile(delete=False)
        f.close()

        if self.verbose:
            locker1 = pylock(f.name, "lock", verbose="1")
            locker2 = pylock(f.name, "lock", verbose="2")
        else:
            locker1 = pylock(f.name, "lock")
            locker2 = pylock(f.name, "lock")

        locker1.lock()
        self.assertRaises(AlreadyLocked, locker2.lock)
        locker1.free()

        locker2.lock()
        self.assertRaises(AlreadyLocked, locker1.lock)
        locker2.free()

        # Remove the temporal file
        os.unlink(f.name)


# Base call
if __name__ == "__main__":
    unittest.main()
