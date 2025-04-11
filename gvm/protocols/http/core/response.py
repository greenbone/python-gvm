# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module for abstracting HTTP responses
"""

from dataclasses import dataclass
from typing import Any, MutableMapping, Optional, Type, TypeVar

from httpx import Response

from gvm.protocols.http.core.headers import ContentType

Self = TypeVar("Self", bound="HttpResponse")


@dataclass
class HttpResponse:
    """
    Class representing an HTTP response.
    """

    body: Any
    "The body of the response"

    status: int
    "HTTP status code of the response"

    headers: MutableMapping[str, str]
    "Dict containing the headers of the response"

    content_type: Optional[ContentType]
    "The content type of the response if it was included in the headers"

    @classmethod
    def from_requests_lib(cls: Type[Self], r: Response) -> "HttpResponse":
        """
        Creates a new HTTP response object from a Request object created by the "Requests" library.

        Args:
            r: The request object to convert.

        Return:
            A HttpResponse object representing the response.

            An empty body is represented by None.
            If the content-type header in the response is set to 'application/json'.
            A non-empty body will be parsed accordingly.
        """
        ct = ContentType.from_string(r.headers.get("content-type"))
        body: Optional[bytes] = r.content

        if r.content == b"":
            body = None
        elif ct is not None:
            if ct.media_type.lower() == "application/json":
                body = r.json()

        return HttpResponse(body, r.status_code, r.headers, ct)
