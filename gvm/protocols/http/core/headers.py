# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module for handling special HTTP headers
"""

from dataclasses import dataclass
from typing import Dict, Optional, Type, TypeVar, Union

Self = TypeVar("Self", bound="ContentType")


@dataclass
class ContentType:
    """
    Class representing the content type of a HTTP response.
    """

    media_type: str
    'The MIME media type, e.g. "application/json"'

    params: Dict[str, Union[bool, str]]
    "Dictionary of parameters in the content type header"

    charset: Optional[str]
    "The charset parameter in the content type header if it is set"

    @classmethod
    def from_string(
        cls: Type[Self],
        header_string: Optional[str],
        fallback_media_type: str = "application/octet-stream",
    ) -> "ContentType":
        """
        Parse the content of content type header into a ContentType object.

        Args:
            header_string: The string to parse
            fallback_media_type: The media type to use if the `header_string` is `None` or empty.
        """
        media_type = fallback_media_type
        params: Dict[str, Union[bool, str]] = {}
        charset = None

        if header_string:
            parts = header_string.split(";")
            if len(parts) > 0:
                media_type = parts[0].strip()
            for part in parts[1:]:
                param = part.strip()
                if "=" in param:
                    key, value = map(lambda x: x.strip(), param.split("=", 1))
                    params[key] = value
                    if key == "charset":
                        charset = value
                else:
                    params[param] = True

        return ContentType(
            media_type=media_type, params=params, charset=charset
        )
