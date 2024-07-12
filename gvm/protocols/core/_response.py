# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property
from typing import Optional, TypeVar

from gvm.errors import GvmError
from gvm.xml import Element, parse_xml

from ._request import Request


class StatusError(GvmError):
    """
    The response had an error status

    May be raised when calling `response.raise_for_status()`
    """

    def __init__(self, message: Optional[str], *args, response: "Response"):
        super().__init__(message, *args)
        self.response = response
        self.request = response.request


Self = TypeVar("Self", bound="Response")


class Response:
    """
    A GMP Response
    """

    def __init__(self, *, request: Request, data: bytes) -> None:
        """
        Create a Response object

        Args:
            request: The request corresponding to this response
            data: The data of the response
        """
        self._request = request
        self._data = data
        self.__xml: Optional[Element] = None

    def __root_element(self) -> Element:
        if self.__xml is None:
            self.__xml = self.xml()
        return self.__xml

    def xml(self) -> Element:
        """
        Return the response data as XML Element

        Raises XmlError if the data is not valid XML.
        """
        return parse_xml(self.data)

    @property
    def data(self) -> bytes:
        """
        Return the data of the response as bytes
        """
        return self._data

    @property
    def request(self) -> Request:
        """
        Return the corresponding request of this response
        """
        return self._request

    @cached_property
    def status_code(self) -> Optional[int]:
        """
        The status code of the response

        Returns:
            The status code or None if the response data doesn't contain a valid
            status code.
        """
        root = self.__root_element()
        try:
            status = root.attrib["status"]
            return int(status)
        except (KeyError, ValueError):
            return None

    @property
    def is_success(self) -> bool:
        """
        Returns True if the response contains a success status code
        """
        status = self.status_code
        return status is not None and 200 <= status <= 299

    def raise_for_status(self: Self) -> Self:
        if self.is_success:
            return self
        raise StatusError(
            f"Invalid status code {self.status_code}", response=self
        )

    def __bytes__(self) -> bytes:
        """
        Return the data as bytes
        """
        return self._data

    def __str__(self) -> str:
        """
        Return the data as string
        """
        return self._data.decode()
