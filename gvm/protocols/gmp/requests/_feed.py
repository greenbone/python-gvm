# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class FeedType(Enum):
    """Enum for feed types"""

    NVT = "NVT"
    CERT = "CERT"
    SCAP = "SCAP"
    GVMD_DATA = "GVMD_DATA"


class Feed:
    @staticmethod
    def get_feeds() -> Request:
        """Request the list of feeds"""
        return XmlCommand("get_feeds")

    @classmethod
    def get_feed(cls, feed_type: Union[FeedType, str]) -> Request:
        """Request a single feed

        Arguments:
            feed_type: Type of single feed to get: NVT, CERT or SCAP
        """
        if not feed_type:
            raise RequiredArgument(
                function=cls.get_feed.__name__, argument="feed_type"
            )

        if not isinstance(feed_type, FeedType):
            feed_type = FeedType(feed_type)

        cmd = XmlCommand("get_feeds")
        cmd.set_attribute("type", feed_type.value)

        return cmd
