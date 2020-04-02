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

    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message

    def __repr__(self):
        return '<{} message="{}">'.format(self.__class__.__name__, self.message)

    def __str__(self):
        return self.message


class GvmClientError(GvmError):
    """An exception for gvm client errors

    Base class for all exceptions originating in python-gvm.
    """


class GvmServerError(GvmError):
    """An exception for gvm server errors

    Derives from :py:class:`GvmError`

    Arguments:
        status:  The HTTP response status
        message: Error message to be displayed. Takes precedence over argument
            and function
    """

    def __init__(self, status: str = None, message: str = None):
        super().__init__(message, status)
        self.status = status

    def __str__(self):
        return 'Server Error {}. {}'.format(self.status, self.message)

    def __repr__(self):
        return '<{} status="{}" message="{}">'.format(
            self.__class__.__name__, self.status, self.message
        )


class GvmResponseError(GvmClientError):
    """An exception for gvm server errors

    Derives from :py:class:`GvmClientError`

    Arguments:
        status:  The HTTP response status
        message: Error message to be displayed. Takes precedence over argument
            and function
    """

    def __init__(self, status: str = None, message: str = None):
        super().__init__(message, status)
        self.status = status

    def __str__(self):
        return 'Response Error {}. {}'.format(self.status, self.message)

    def __repr__(self):
        return '<{} status="{}" message="{}">'.format(
            self.__class__.__name__, self.status, self.message
        )


class InvalidArgument(GvmError):
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
        function: Optional[str] = None
    ):
        super().__init__(message, argument, function)
        self.argument = argument
        self.function = function

    def __str__(self):
        if self.message:
            return self.message

        if not self.function:
            return "Invalid argument {}".format(self.argument)

        if not self.argument:
            return "Invalid argument for {}".format(self.function)

        return "Invalid argument {} for {}".format(self.argument, self.function)


class InvalidArgumentType(GvmError):
    """Raised if a passed argument has an invalid type

    Derives from :py:class:`GvmError`

    Arguments:
        argument: Name of the invalid argument
        arg_type: The correct argument type
        function: Optional name of the called function
    """

    def __init__(
        self,
        argument: str = None,
        arg_type: str = None,
        *,
        function: Optional[str] = None
    ):
        # pylint: disable=super-init-not-called
        self.argument = argument
        self.function = function
        self.arg_type = arg_type

    def __str__(self):
        if self.function:
            return "In {} the argument {} must be of type {}.".format(
                self.function, self.argument, self.arg_type
            )
        return "The argument {} must be of type {}.".format(
            self.argument, self.arg_type
        )


class RequiredArgument(GvmError):
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
        *,
        argument: Optional[str] = None,
        function: Optional[str] = None
    ):
        super().__init__(message, argument, function)
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
