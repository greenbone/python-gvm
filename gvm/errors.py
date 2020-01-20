# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module for GVM errors
"""

from typing import Optional


class GvmError(Exception):
    """An exception for gvm errors

    Base class for all exceptions originating in python-gvm.
    """

class GvmResponseError(GvmError):
    def __init__(
        self,
        status: Optional[str] = None,
        message: Optional[str] = None,
        *,
        argument: Optional[str] = None,
        function: Optional[str] = None
    ):
        # pylint: disable=super-init-not-called
        self.status = status
        self.message = message
        self.argument = argument
        self.function = function

    def __str__(self):
        if self.status and self.message:
            return self.__class__.__name__ + ': ' + self.status + ' - ' + self.message
        else:
            return self.__class__.__name__ + ': ' + getattr(self, 'args')[0]

class GvmClientError(GvmError):
    """An exception for gvm client errors

    Base class for all exceptions originating in python-gvm.
    """

class InvalidArgument(GvmClientError):
    """Raised if an invalid argument/parameter is passed

    Derives from :py:class:`GvmError`

    Arguments:
        message: Error message to be displayed. Takes precedence over argument
            and function
        argument: Optional name of the invalid argument
        function: Optional name of the called function
    """

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        argument: Optional[str] = None,
        function: Optional[str] = None,
        arg_type: Optional[str] = None
    ):
        # pylint: disable=super-init-not-called
        self.message = message
        self.argument = argument
        self.function = function
        self.arg_type = arg_type

    def __str__(self):
        if self.arg_type and self.argument:
            if self.function:
                return "In {} the argument {} must be of type {}.".format(self.function, self.argument, self.arg_type)
            return "The argument {} must be of type {}.".format(self.argument, self.arg_type)
        
        if self.message:
            return self.message

        if not self.function:
            return "Invalid argument {}".format(self.argument)

        if not self.argument:
            return "Invalid argument for {}".format(self.function)

        return "Invalid argument {} for {}".format(self.argument, self.function)

class InvalidArgumentType(GvmClientError):
    def __init__(
        self,
        argument: str = None,
        arg_type: str = None,
        *,
        function: Optional[str] = None,
    ):
        # pylint: disable=super-init-not-called
        self.argument = argument
        self.function = function
        self.arg_type = arg_type

    def __str__(self):
        if self.function:
            return "In {} the argument {} must be of type {}.".format(self.function, self.argument, self.arg_type)
        return "The argument {} must be of type {}.".format(self.argument, self.arg_type)

class RequiredArgument(GvmClientError):
    """Raised if a required argument/parameter is missing

    Derives from :py:class:`GvmError`

    Arguments:
        message: Error message to be displayed. Takes precedence over argument
            and function.
        argument: Optional name of the required argument.
        function: Optional name of the called function.
    """

    def __init__(
        self,
        message: Optional[str] = None,
        argument: Optional[str] = None,
        function: Optional[str] = None,
    ):
        # pylint: disable=super-init-not-called
        self.message = message
        self.argument = argument
        self.function = function

    def __str__(self):
        if self.message:
            return self.message

        if not self.function:
            return "Required argument {}".format(self.argument)

        if not self.argument:
            return "Required argument missing for {}".format(self.function)

        return "{} requires a {} argument".format(self.function, self.argument)
