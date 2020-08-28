# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv7 import AliveTest, get_alive_test_from_string


class GetAliveTestFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_alive_test_from_string('foo')

    def test_none_or_empty(self):
        ct = get_alive_test_from_string(None)
        self.assertIsNone(ct)
        ct = get_alive_test_from_string('')
        self.assertIsNone(ct)

    def test_scan_config_default(self):
        ct = get_alive_test_from_string('Scan Config Default')
        self.assertEqual(ct, AliveTest.SCAN_CONFIG_DEFAULT)

    def test_icmp_ping(self):
        ct = get_alive_test_from_string('ICMP Ping')
        self.assertEqual(ct, AliveTest.ICMP_PING)

    def test_tcp_ack_service_ping(self):
        ct = get_alive_test_from_string('TCP-ACK Service Ping')
        self.assertEqual(ct, AliveTest.TCP_ACK_SERVICE_PING)

    def test_tcp_sync_service_ping(self):
        ct = get_alive_test_from_string('TCP-SYN Service Ping')
        self.assertEqual(ct, AliveTest.TCP_SYN_SERVICE_PING)

    def test_arp_ping(self):
        ct = get_alive_test_from_string('ARP Ping')
        self.assertEqual(ct, AliveTest.ARP_PING)

    def test_icmp_and_tcp_ack_service_ping(self):
        ct = get_alive_test_from_string('ICMP & TCP-ACK Service Ping')
        self.assertEqual(ct, AliveTest.ICMP_AND_TCP_ACK_SERVICE_PING)

    def test_icmp_and_arp_ping(self):
        ct = get_alive_test_from_string('ICMP & ARP Ping')
        self.assertEqual(ct, AliveTest.ICMP_AND_ARP_PING)

    def test_tcp_ack_service_and_arp_ping(self):
        ct = get_alive_test_from_string('TCP-ACK Service & ARP Ping')
        self.assertEqual(ct, AliveTest.TCP_ACK_SERVICE_AND_ARP_PING)

    def test_icmp_tcp_ack_service_and_arp_ping(self):
        ct = get_alive_test_from_string('ICMP, TCP-ACK Service & ARP Ping')
        self.assertEqual(ct, AliveTest.ICMP_TCP_ACK_SERVICE_AND_ARP_PING)

    def test_consider_alive(self):
        ct = get_alive_test_from_string('Consider Alive')
        self.assertEqual(ct, AliveTest.CONSIDER_ALIVE)


if __name__ == '__main__':
    unittest.main()
