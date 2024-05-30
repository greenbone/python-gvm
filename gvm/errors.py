# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Module for GVM errors
"""

from typing import Optional


class GvmError(Exception):
    """An exception for gvm errors

    Base class for all exceptions originating in python-gvm.
    """

    def __init__(self, message: Optional[str], *args):
        super().__init__(message, *args)
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
        self, status: Optional[str] = None, message: Optional[str] = None
    ):
        super().__init__(message, status)
        self.status = status

    def __str__(self):
        return f"Server Error {self.status}. {self.message}"

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} status="{self.status}"'
            f' message="{self.message}">'
        )


class GvmResponseError(GvmClientError):
    """An exception for gvm server errors

    Derives from :py:class:`GvmClientError`

    Arguments:
        status:  The HTTP response status
        message: Error message to be displayed. Takes precedence over argument
            and function
    """

    def __init__(
        self, status: Optional[str] = None, message: Optional[str] = None
    ):
        super().__init__(message, status)
        self.status = status

    def __str__(self):
        return f"Response Error {self.status}. {self.message}"

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} status="{self.status}"'
            f' message="{self.message}">'
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
        function: Optional[str] = None,
    ):
        super().__init__(message, argument, function)
        self.argument = argument
        self.function = function

    def __str__(self):
        if self.message:
            return self.message

        if not self.function:
            return f"Invalid argument {self.argument}"

        if not self.argument:
            return f"Invalid argument for {self.function}"

        return f"Invalid argument {self.argument} for {self.function}"


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
        argument: str,
        *,
        arg_type: Optional[str] = None,
        function: Optional[str] = None,
    ):
        super().__init__(None)
        self.argument = argument
        self.function = function
        self.arg_type = arg_type

    def __str__(self):
        if self.function:
            if self.arg_type:
                return (
                    f"In {self.function} the argument {self.argument} "
                    f"must be of type {self.arg_type}."
                )
            return (
                f"Invalid argument type for argument {self.argument} in "
                f"{self.function}."
            )
        if self.arg_type:
            return (
                f"The argument {self.argument} must be of type {self.arg_type}."
            )

        return f"Invalid argument type for argument {self.argument}."


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
        function: Optional[str] = None,
    ):
        super().__init__(message, argument, function)
        self.argument = argument
        self.function = function

    def __str__(self):
        if self.message:
            return self.message

        if not self.function:
            return f"Required argument {self.argument}"

        if not self.argument:
            return f"Required argument missing for {self.function}"

        return f"{self.function} requires a {self.argument} argument"
