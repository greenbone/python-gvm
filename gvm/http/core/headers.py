# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module for handling special HTTP headers
"""

from dataclasses import dataclass
from typing import Self, Dict, Optional


@dataclass
class ContentType:
    """
    Class representing the content type of a HTTP response.
    """

    media_type: str
    "The MIME media type, e.g. \"application/json\""

    params: Dict[str,str]
    "Dictionary of parameters in the content type header"

    charset: Optional[str]
    "The charset parameter in the content type header if it is set"

    @classmethod
    def from_string(
        cls,
        header_string: str,
        fallback_media_type: Optional[str] = "application/octet-stream"
    ) -> Self:
        """
        Parse the content of content type header into a ContentType object.

        Args:
            header_string: The string to parse
            fallback_media_type: The media type to use if the `header_string` is `None` or empty.
        """
        media_type = fallback_media_type
        params = {}
        charset = None

        if header_string:
            parts = header_string.split(";")
            media_type = parts[0].strip()
            for param in parts[1:]:
                param = param.strip()
                if "=" in param:
                    key, value = map(lambda x: x.strip(), param.split("=", 1))
                    params[key] = value
                    if key == 'charset':
                        charset = value
                else:
                    params[param] = True

        return ContentType(media_type=media_type, params=params, charset=charset)
