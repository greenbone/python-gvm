# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 Greenbone Networks GmbH
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

from gvm.errors import RequiredArgument
from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPStopScanTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_stop_scan(self):
        self.osp.stop_scan(scan_id="123-456")

        self.connection.send.has_been_called_with(
            '<stop_scan scan_id="123-456"/>'
        )

    def test_stop_scan_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.osp.stop_scan(None)

        with self.assertRaises(RequiredArgument):
            self.osp.stop_scan('')


if __name__ == '__main__':
    unittest.main()
