# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from gvm.connections import GvmConnection, DEFAULT_TIMEOUT


class GvmConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access
    def test_init_no_args(self):
        connection = GvmConnection()
        self.check_for_default_values(connection)

    def test_init_with_none(self):
        connection = GvmConnection(timeout=None)
        self.check_for_default_values(connection)

    def check_for_default_values(self, gvm_connection: GvmConnection):
        self.assertIsNone(gvm_connection._socket)
        self.assertEqual(gvm_connection._timeout, DEFAULT_TIMEOUT)
