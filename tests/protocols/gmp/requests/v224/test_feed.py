# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Feed, FeedType


class FeedTestCase(unittest.TestCase):
    def test_get_feed(self) -> None:
        """
        Test basic get_feed calls with only resource_type except special
        cases for audit, policy, scan_config and task.
        """
        request = Feed.get_feed(FeedType.NVT)

        self.assertEqual(bytes(request), b'<get_feeds type="NVT"/>')

        request = Feed.get_feed(FeedType.CERT)

        self.assertEqual(bytes(request), b'<get_feeds type="CERT"/>')

        request = Feed.get_feed(FeedType.SCAP)

        self.assertEqual(bytes(request), b'<get_feeds type="SCAP"/>')

        request = Feed.get_feed(FeedType.GVMD_DATA)

        self.assertEqual(bytes(request), b'<get_feeds type="GVMD_DATA"/>')

    def test_get_feed_missing_type(self):
        """
        Test get_feed calls with missing resource_type
        """
        with self.assertRaises(RequiredArgument):
            Feed.get_feed(feed_type=None)

        with self.assertRaises(RequiredArgument):
            Feed.get_feed(feed_type="")

        with self.assertRaises(RequiredArgument):
            Feed.get_feed("")

    def test_get_feed_invalid_type(self):
        """
        Test get_feed calls with invalid resource_type
        """
        with self.assertRaises(InvalidArgument):
            Feed.get_feed("foo")
