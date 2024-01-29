# SPDX-FileCopyrightText: 2022-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
