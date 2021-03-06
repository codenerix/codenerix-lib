# -*- coding: utf-8 -*-
#
# django-codenerix
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
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

'''
Debugger helps to debug the system
'''

from os import getcwd
from time import time
from datetime import datetime
from inspect import currentframe

from .colors import colors

__version__ = "2019051003"

__all__ = ['Debugger', 'lineno', '__FILE__', '__LINE__']


def lineno():
    '''
    Returns the current line number in our program.
    '''
    return currentframe().f_back.f_lineno


def __LINE__():
    '''
    Returns the current line number in our program.
    '''
    return currentframe().f_back.f_lineno


def __FILE__():
    '''
    Returns the current line number in our program.
    '''
    filename = currentframe().f_back.f_code.co_filename.replace(getcwd(), ".")
    if len(filename) >= 2 and filename[0] == "." and filename[1] == "/":
        filename = filename[2:]
    return filename


class Debugger(object):

    __indebug = {}
    __inname = None

    KINDS = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'error']

    def __autoconfig(self):
        # Define debug configuration
        import sys
        debugger = {}
        debugger['screen'] = (sys.stdout, ['*'])
        # debugger['log'] = (open("log/debug.log","a"), ['*'] )
        self.set_debug(debugger)

    def set_debug(self, debug=None):
        if debug is None:
            self.__autoconfig()
        else:
            if type(debug) is dict:
                # Set the deepness system
                idebug = debug.copy()
                if 'deepness' in debug:
                    if debug['deepness']:
                        idebug['deepness'] -= 1
                    else:
                        for key in idebug:
                            if key not in ['tabular', 'deepness']:
                                newlist = []
                                for element in idebug[key][1]:
                                    if element in ['-*error', '-*warning']:
                                        newlist.append(element)
                                idebug[key][1] = newlist

                # Save internal debugger
                self.__indebug = idebug
            else:
                raise IOError("Argument is not a dictionary")

    def set_origin(self, origin):
        self.origin = origin

    def get_debug(self):
        return self.__indebug

    def set_name(self, name):
        self.__inname = name

    def get_name(self):
        return self.__inname

    def color(self, color):
        # Colors$
        if color in colors:
            (darkbit, subcolor) = colors[color]
            return u"\033[%1d;%02dm" % (darkbit, subcolor)
        else:
            if color:
                self.debug(u"\033[1;31mColor '%s' unknown\033[1;00m\n" % (color))
            return ''

    def debug(self, msg=None, header=None, color=None, tail=None, head=None, footer=None, origin=False, kind=""):

        # If origin has been requested
        if origin or getattr(self, 'origin', False):
            origin = True
            line = currentframe().f_back.f_lineno
            filename = currentframe().f_back.f_code.co_filename.replace(getcwd(), ".")
            if len(filename) >= 2 and filename[0] == "." and filename[1] == "/":
                filename = filename[2:]

        # Allow better names for debug calls
        if header is None:
            if head is None:
                header = True
            else:
                header = head
        if tail is None:
            if footer is None:
                tail = True
            else:
                tail = footer

        # Retrieve the name of the class
        clname = self.__class__.__name__

        # Retrieve tabular
        if 'tabular' in self.__indebug:
            tabular = self.__indebug['tabular']
        else:
            tabular = ''

        # For each element inside indebug
        for name in self.__indebug:

            # If this is no deepeness key, keep going
            if name not in ['deepness', 'tabular']:

                # Get color
                if name == 'screen' or name[-1] == '*':
                    color_ini = self.color(color)
                    color_end = self.color('close')
                else:
                    color_ini = self.color(None)
                    color_end = color_ini

                # Get file output handler and indebug list
                (handler, indebug) = self.__indebug[name]

                if not kind or "-*{}".format(kind) not in indebug:
                    if msg and type(handler) == str:
                        # Open handler buffer
                        handlerbuf = open(handler, "a")
                    else:
                        handlerbuf = handler

                    # Look up if the name of the class is inside indebug
                    if (clname in indebug) or (('*' in indebug) and ('-%s' % (clname) not in indebug)):

                        # Set line head name
                        if self.__inname:
                            headname = self.__inname
                        else:
                            headname = clname

                        # Build the message
                        message = color_ini
                        if header:
                            now = datetime.fromtimestamp(time())
                            message += "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d} ".format(now.day, now.month, now.year, now.hour, now.minute, now.second)
                            if origin:
                                message += "{}:{}: ".format(filename, line)
                            message += "{:<15s} - {}".format(headname, tabular)

                        if msg:
                            try:
                                message += str(msg)
                            except UnicodeEncodeError:
                                message += str(msg.encode('ascii', 'ignore'))
                        message += color_end
                        if tail:
                            message += '\n'

                        # Print it on the buffer handler
                        if msg:
                            handlerbuf.write(message)
                            handlerbuf.flush()
                        else:
                            # If we shouldn't show the output, say to the caller we should output something
                            return True

                    # Autoclose handler when done
                    if msg and type(handler) == str:
                        handlerbuf.close()

        # If we shouldn't show the output
        if not msg:
            # Say to the caller we shouldn't output anything
            return False

    def debug_with_style(self, msg, title, color, kind, show_line_info, header=True, tail=True):
        if show_line_info:
            line = currentframe().f_back.f_lineno
            filename = currentframe().f_back.f_code.co_filename.replace(getcwd(), ".")
            if len(filename) >= 2 and filename[0] == "." and filename[1] == "/":
                filename = filename[2:]
        else:
            line = None
            filename = None
        self.warningerror(msg, header, title, color, tail, line=line, filename=filename, kind=kind)

    def primary(self, msg, header=True, tail=True, show_line_info=False):
        self.debug_with_style(msg, "PRIMARY", "blue", "primary", show_line_info, header=header, tail=tail)

    def secondary(self, msg, header=True, tail=True, show_line_info=False):
        self.debug_with_style(msg, "SECONDARY", "purple", "secondary", show_line_info, header=header, tail=tail)

    def success(self, msg, header=True, tail=True, show_line_info=False):
        self.debug_with_style(msg, "SUCCESS", "green", "success", show_line_info, header=header, tail=tail)

    def danger(self, msg, header=True, tail=True, show_line_info=False):
        self.debug_with_style(msg, "DANGER", "simplered", "danger", show_line_info, header=header, tail=tail)

    def warning(self, msg, header=True, tail=True, show_line_info=True):
        self.debug_with_style(msg, "WARNING", "yellow", "warning", show_line_info, header=header, tail=tail)

    def info(self, msg, header=True, tail=True, show_line_info=False):
        self.debug_with_style(msg, "INFO", "cyan", "info", show_line_info, header=header, tail=tail)

    def error(self, msg, header=True, tail=True, show_line_info=True):
        self.debug_with_style(msg, "ERROR", "red", "error", show_line_info, header=header, tail=tail)

    def warningerror(self, msg, header, prefix, color, tail, line=None, filename=None, kind=None):

        # Retrieve the name of the class
        clname = self.__class__.__name__

        # Retrieve tabular
        if 'tabular' in self.__indebug:
            tabular = self.__indebug['tabular']
        else:
            tabular = ''

        # For each element inside indebug
        for name in self.__indebug:

            # If this is no deepeness key, keep going
            if name not in ['deepness', 'tabular']:

                # Get file output handler and indebug list
                (handler, indebug) = self.__indebug[name]

                if "-*{}".format(kind) not in indebug:
                    if type(handler) == str:
                        # Open handler buffer
                        handlerbuf = open(handler, "a")
                    else:
                        handlerbuf = handler

                    # Get color
                    if name == 'screen' or name[-1] == '*':
                        color_ini = self.color(color)
                        color_end = self.color('close')
                    else:
                        color_ini = self.color(None)
                        color_end = color_ini

                    # Build the message
                    message = color_ini
                    if header:
                        # Set line head name
                        if self.__inname:
                            headname = self.__inname
                        else:
                            headname = clname

                        now = datetime.fromtimestamp(time())
                        message += "\n%s - %02d/%02d/%d %02d:%02d:%02d " % (prefix, now.day, now.month, now.year, now.hour, now.minute, now.second)
                        if filename or line:
                            message += "{}:{}: ".format(filename, line)
                        message += "%-15s - %s" % (headname, tabular)
                    if msg:
                        try:
                            message += str(msg)
                        except UnicodeEncodeError:
                            try:
                                message += str(msg.encode('ascii', 'ignore'))
                            except Exception:
                                message += "*** Message is in Binary format, I tried to convert to ASCII ignoring encoding errors but it failed as well. ***"
                    message += color_end
                    if tail:
                        message += '\n'

                    # Print it on the buffer handler
                    handlerbuf.write(message)
                    handlerbuf.flush()

                    # Autoclose handler when done
                    if type(handler) == str:
                        handlerbuf.close()
