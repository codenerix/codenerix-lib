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
Timeout exception definition and timeout function to allow the user to call
functions under specific timeout. The function will raise an exception when
timeout is reached if the called function didn't finish execution before
"""

__version__ = "2017112900"

import ctypes
import queue
import signal
import threading
import time

__all__ = ["TimedOutException", "timeout", "timeout2"]


class TimedOutException(Exception):
    """
    Timeout exception definition
    """

    def __init__(self, value="Timed Out"):
        """
        Parameters:
        - `value`: text to raise in the exception
        """
        self.value = value

    def __str__(self):
        return str(self.value)


def timeout(f, timeout, *args, **kwargs):
    """
    Function that controls the timeout

    Parameters:
    - `f`: function to process under timeout control
    - `timeout`: total number of seconds to wait until timeout (not allowed 0
      or less)
    - `args` & `kwargs`: to allow in this function any kind of parameters
       to be passed to function f

    Exceptions:
    - `IOError`: parameter error
    - `TimedOutException`: when timeout reach to the limit and the function is
       still executing
    """

    # Control that timeout can not be zero or negative
    if timeout <= 0:
        raise OSError("Timeout can not be zero or less than zero")

    # Define the handler
    def handler(signum, frame):
        raise TimedOutException()

    # Remember the actual signal handler
    old = signal.signal(signal.SIGALRM, handler)

    # Install timeout control
    signal.alarm(timeout)

    try:
        # Launch the function with all arguments
        result = f(*args, **kwargs)
    finally:
        # Restore old signal handler
        signal.signal(signal.SIGALRM, old)
        # Remove timeout control
        signal.alarm(0)

    # Return the result of the function
    return result


class ThreadedCMD(threading.Thread):
    def __init__(self, result, f, args=(), kwargs={}):
        # Initialice thread
        super().__init__()

        # Save incoming data
        self.__f = f
        self.__args = args
        self.__kwargs = kwargs
        self.__result = result

        # Save exceptions if any
        self.__exception = None

    def run(self):
        # Call function an set result
        try:
            # Launch f()
            result = self.__f(*self.__args, **self.__kwargs)
            # Set result in the queue
            self.__result.put(result)
        except (Exception, KeyboardInterrupt) as e:  # pragma: no cover
            self.__exception = e

    def exception(self):
        if self.__exception:
            return self.__exception  # pragma: no cover
        else:
            return None


def terminate_thread(thread):  # pragma: no cover
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.is_alive():
        return  # pragma: no cover

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident),
        exc,
    )
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def timeout2(f, timeout, quit=None, reactivity=0.1, args=(), kwargs={}):
    """
    Function that controls the timeout of another function using only threads

    Parameters:
    - `f`: function to process under timeout control
    - `timeout`: total number of seconds to wait until timeout (not
         allowed 0 or less)
    - `quit`: function called with no arguments to request f() to finish
    - `reactivity`: time that the algorithm will wait between checks (faster
         means more CPU it will consume)
    - `args` & `kwargs`: to allow in this function any kind of parameters to
         be passed to function f

    Exceptions:
    - `IOError`: parameter error
    - `TimedOutException`: when timeout reach to the limit and the function is
       still executing
    """

    # Set startup
    startup = time.time()

    # Control that timeout can not be zero or negative
    if timeout <= 0:
        raise OSError("Timeout can not be zero or less than zero")

    # Prepare queue
    result = queue.Queue()

    th = ThreadedCMD(result, f, args, kwargs)
    th.start()

    # Wait until done
    while th.is_alive():
        diff = time.time() - startup
        if diff > timeout:
            # It has passed too much time, finish this!
            break
        else:
            # Wait for another loop
            try:
                time.sleep(reactivity)
            except (Exception, KeyboardInterrupt):  # pragma: no cover
                break

    # Get exceptions if any
    ex = th.exception()

    # If the thread is still working and we are here, we must stop it!
    if th.is_alive():
        # Stop the thread
        if quit:
            quit()  # pragma: no cover
        terminate_thread(th)
        # Raise exception since we didn't finish on time
        if ex:
            raise ex  # pragma: no cover
        else:
            raise TimedOutException()
    else:
        # Return the result of the function
        if ex:
            raise ex  # pragma: no cover
        else:
            try:
                return result.get(False)
            except (Exception, KeyboardInterrupt):  # pragma: no cover
                return None
