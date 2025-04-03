# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from typing import Any, Dict, Self, Optional
from requests import Request, Response

from gvm.http.core.headers import ContentType


@dataclass
class HttpResponse:
    """
    Class representing an HTTP response.
    """
    body: Any
    status: int
    headers: Dict[str, str]
    content_type: Optional[ContentType]

    @classmethod
    def from_requests_lib(cls, r: Response) -> Self:
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
        ct = ContentType.from_string(r.headers.get('content-type'))
        body = r.content

        if r.content == b'':
            body = None
        elif ct is not None:
            if ct.media_type.lower() == 'application/json':
                body = r.json()

        return HttpResponse(body, r.status_code, r.headers, ct)
