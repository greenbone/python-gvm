# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.xml import XmlCommand


class FeedType(Enum):
    """Enum for feed types"""

    NVT = "NVT"
    CERT = "CERT"
    SCAP = "SCAP"
    GVMD_DATA = "GVMD_DATA"

    @classmethod
    def from_string(cls, feed_type: Optional[str]) -> Optional["FeedType"]:
        """Convert a feed type string into a FeedType instance"""
        if not feed_type:
            return None

        try:
            return cls[feed_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="feed_type", function=cls.from_string.__name__
            ) from None


class FeedMixin:
    def get_feeds(self) -> Any:
        """Request the list of feeds

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_feeds"))

    def get_feed(self, feed_type: Optional[FeedType]) -> Any:
        """Request a single feed

        Arguments:
            feed_type: Type of single feed to get: NVT, CERT or SCAP

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not feed_type:
            raise RequiredArgument(
                function=self.get_feed.__name__, argument="feed_type"
            )

        if not isinstance(feed_type, FeedType):
            raise InvalidArgumentType(
                function=self.get_feed.__name__,
                argument="feed_type",
                arg_type=FeedType.__name__,
            )

        cmd = XmlCommand("get_feeds")
        cmd.set_attribute("type", feed_type.value)

        return self._send_xml_command(cmd)
