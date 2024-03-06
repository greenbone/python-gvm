# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property
from typing import Optional

from typing_extensions import Self

from gvm.errors import GvmError
from gvm.xml import Element, parse_xml

from ._request import Request


class StatusError(GvmError):
    def __init__(self, message: str | None, *args, response: "Response"):
        super().__init__(message, *args)
        self.response = response
        self.request = response.request


class Response:
    def __init__(self, *, request: Request, data: bytes) -> None:
        self._request = request
        self._data = data
        self.__xml: Optional[Element] = None

    def __root_element(self) -> Element:
        if self.__xml is None:
            self.__xml = self.xml()
        return self.__xml

    def xml(self) -> Element:
        return parse_xml(self.data)

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def request(self) -> Request:
        return self._request

    @cached_property
    def status_code(self) -> Optional[int]:
        root = self.__root_element()
        try:
            status = root.attrib["status"]
            return int(status)
        except (KeyError, ValueError):
            return None

    @property
    def is_success(self) -> bool:
        status = self.status_code
        return status is not None and 200 <= status <= 299

    def raise_for_status(self) -> Self:
        if self.is_success:
            return self
        raise StatusError(
            f"Invalid status code {self.status_code}", response=self
        )

    def __bytes__(self) -> bytes:
        return self._data

    def __str__(self) -> str:
        return self._data.decode()
