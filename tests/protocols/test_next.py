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

# pylint: disable=no-member

import unittest

from gvm.protocols.next import Gmp, Osp


class LatestProtocolsTestCase(unittest.TestCase):
    def test_gmp_version(self):
        self.assertEqual(Gmp.get_protocol_version(), (22, 4))

    def test_osp_version(self):
        self.assertEqual(Osp.get_protocol_version(), (1, 2))


if __name__ == "__main__":
    unittest.main()
