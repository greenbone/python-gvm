# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import FeedType


class GmpGetFeedTestMixin:
    def test_get_feed(self):
        """
        Test basic get_feed calls with only resource_type except special
        cases for audit, policy, scan_config and task.
        """
        self.gmp.get_feed(FeedType.NVT)

        self.connection.send.has_been_called_with(b'<get_feeds type="NVT"/>')

        self.gmp.get_feed(FeedType.CERT)

        self.connection.send.has_been_called_with(b'<get_feeds type="CERT"/>')

        self.gmp.get_feed(FeedType.SCAP)

        self.connection.send.has_been_called_with(b'<get_feeds type="SCAP"/>')

        self.gmp.get_feed(FeedType.GVMD_DATA)

        self.connection.send.has_been_called_with(
            b'<get_feeds type="GVMD_DATA"/>'
        )

    def test_get_feed_missing_type(self):
        """
        Test get_feed calls with missing resource_type
        """
        with self.assertRaises(RequiredArgument):
            self.gmp.get_feed(feed_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_feed(feed_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_feed("")

    def test_get_feed_invalid_type(self):
        """
        Test get_feed calls with invalid resource_type
        """
        with self.assertRaises(InvalidArgument):
            self.gmp.get_feed("foo")
