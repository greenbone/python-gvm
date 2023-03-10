# -*- coding: utf-8 -*-
# Copyright (C) 2022 Greenbone AG
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

from gvm.utils import check_port


class TestCheckPort(unittest.TestCase):
    def test_port_cpe(self):
        self.assertTrue(check_port("cpe:meh:moo*"))

    def test_port_cpe_fail(self):
        self.assertFalse(check_port("cpe:meh haha"))

    def test_port_general(self):
        self.assertTrue(check_port("general/tcp"))

    def test_ports(self):
        self.assertTrue(check_port("1/tcp"))
        self.assertTrue(check_port("12/tcp"))
        self.assertTrue(check_port("123/tcp"))
        self.assertTrue(check_port("1234/tcp"))
        self.assertTrue(check_port("12345/tcp"))
        self.assertTrue(check_port("1/udp"))
        self.assertTrue(check_port("12/udp"))

    def test_ports_fail(self):
        self.assertFalse(check_port("1"))
        self.assertFalse(check_port("1//udp"))
        self.assertFalse(check_port("1/12/tcp"))
        self.assertFalse(check_port("tcp"))
        self.assertFalse(check_port("general"))
        self.assertFalse(check_port("lol"))
