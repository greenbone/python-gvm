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

from typing import Optional

"""
Module for GVM errors
"""


class GvmError(Exception):
    """An exception for gvm errors

    Base class for all exceptions originating in python-gvm.
    """

    def __init__(self, *args: Optional[tuple], message: str = None):
        super().__init__(*args, message)
        self.message = message

    def __repr__(self):
        return f'<{self.__class__.__name__} message="{self.message}">'

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

    def __init__(
        self, *args: Optional[tuple], status: str = None, message: str = None
    ):
        message = f'Server Error "{status}": {message}'
        super().__init__(*args, message=message)
        self.status = status


class GvmResponseError(GvmClientError):
    """An exception for gvm response errors

    Derives from :py:class:`GvmClientError`

    Arguments:
        status:  The HTTP response status
        message: Error message to be displayed. Takes precedence over argument
            and function
    """

    def __init__(
        self, *args: Optional[tuple], status: str = None, message: str = None
    ):
        message = f'Response Error "{status}": {message}'
        super().__init__(*args, message=message)
        self.status = status


class InvalidArgument(GvmError):
    """Raised if an invalid argument/parameter is passed

    Derives from :py:class:`GvmError`

    Arguments:
        argument: Optional name of the invalid argument
        function: Optional name of the called function
    """

    def __init__(
        self, *args: Optional[tuple], argument: str = None, function: str = None
    ):
        message = f'Invalid argument: "{argument}" is invalid in {function}'
        super().__init__(*args, message=message)


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
        *args: Optional[tuple],
        argument: str = None,
        arg_type: str = None,
        function: str = None
    ):
        message = f'Invalid argument type: "{argument}" must be of type "{arg_type}" in {function}.'
        super().__init__(*args, message=message)


class RequiredArgument(GvmError):
    """Raised if a required argument/parameter is missing

    Derives from :py:class:`GvmError`

    Arguments:
        argument: Optional name of the required argument.
        function: Optional name of the called function.
    """

    def __init__(
        self, *args: Optional[tuple], argument: str = None, function: str = None
    ):
        message = f'Required argument: "{argument}" is required in {function}'
        super().__init__(*args, message=message)
