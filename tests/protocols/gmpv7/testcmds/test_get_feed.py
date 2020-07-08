# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import unittest

from gvm.errors import RequiredArgument, InvalidArgumentType

from gvm.protocols.gmpv7 import FeedType


class GmpGetFeedTestCase:
    def test_get_feed(self):
        self.gmp.get_feed(FeedType.NVT)

        self.connection.send.has_been_called_with('<get_feeds type="NVT"/>')

        self.gmp.get_feed(feed_type=FeedType.NVT)

        self.connection.send.has_been_called_with('<get_feeds type="NVT"/>')

        self.gmp.get_feed(FeedType.CERT)

        self.connection.send.has_been_called_with('<get_feeds type="CERT"/>')

        self.gmp.get_feed(FeedType.SCAP)

        self.connection.send.has_been_called_with('<get_feeds type="SCAP"/>')

    def test_get_feed_missing_feed_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_feed(feed_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_feed('')

    def test_get_feed_invalid_feed_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_feed(feed_type='foo')


if __name__ == '__main__':
    unittest.main()
