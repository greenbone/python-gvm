# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208 import FeedType


class GmpGetFeedTestMixin:
    def test_get_feed(self):
        """
        Test basic get_feed calls with only resource_type except special
        cases for audit, policy, scan_config and task.
        """
        self.gmp.get_feed(FeedType.NVT)

        self.connection.send.has_been_called_with('<get_feeds type="NVT"/>')

        self.gmp.get_feed(FeedType.CERT)

        self.connection.send.has_been_called_with('<get_feeds type="CERT"/>')

        self.gmp.get_feed(FeedType.SCAP)

        self.connection.send.has_been_called_with('<get_feeds type="SCAP"/>')

        self.gmp.get_feed(FeedType.GVMD_DATA)

        self.connection.send.has_been_called_with(
            '<get_feeds type="GVMD_DATA"/>'
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
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_feed("foo")
