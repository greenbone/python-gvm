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

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPGetVtsTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_get_vts_with_vt(self):
        self.osp.get_vts(vt_id="1.1.1.1.1.1")

        self.connection.send.has_been_called_with(
            '<get_vts vt_id="1.1.1.1.1.1"/>'
        )

    def test_get_vts(self):
        self.osp.get_vts()

        self.connection.send.has_been_called_with('<get_vts/>')


if __name__ == '__main__':
    unittest.main()
