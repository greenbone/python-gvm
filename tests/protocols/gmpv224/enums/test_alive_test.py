# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import AliveTest


class GetAliveTestFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            AliveTest.from_string("foo")

    def test_none_or_empty(self):
        ct = AliveTest.from_string(None)
        self.assertIsNone(ct)
        ct = AliveTest.from_string("")
        self.assertIsNone(ct)

    def test_scan_config_default(self):
        ct = AliveTest.from_string("Scan Config Default")
        self.assertEqual(ct, AliveTest.SCAN_CONFIG_DEFAULT)

    def test_icmp_ping(self):
        ct = AliveTest.from_string("ICMP Ping")
        self.assertEqual(ct, AliveTest.ICMP_PING)

    def test_tcp_ack_service_ping(self):
        ct = AliveTest.from_string("TCP-ACK Service Ping")
        self.assertEqual(ct, AliveTest.TCP_ACK_SERVICE_PING)

    def test_tcp_sync_service_ping(self):
        ct = AliveTest.from_string("TCP-SYN Service Ping")
        self.assertEqual(ct, AliveTest.TCP_SYN_SERVICE_PING)

    def test_arp_ping(self):
        ct = AliveTest.from_string("ARP Ping")
        self.assertEqual(ct, AliveTest.ARP_PING)

    def test_icmp_and_tcp_ack_service_ping(self):
        ct = AliveTest.from_string("ICMP & TCP-ACK Service Ping")
        self.assertEqual(ct, AliveTest.ICMP_AND_TCP_ACK_SERVICE_PING)

    def test_icmp_and_arp_ping(self):
        ct = AliveTest.from_string("ICMP & ARP Ping")
        self.assertEqual(ct, AliveTest.ICMP_AND_ARP_PING)

    def test_tcp_ack_service_and_arp_ping(self):
        ct = AliveTest.from_string("TCP-ACK Service & ARP Ping")
        self.assertEqual(ct, AliveTest.TCP_ACK_SERVICE_AND_ARP_PING)

    def test_icmp_tcp_ack_service_and_arp_ping(self):
        ct = AliveTest.from_string("ICMP, TCP-ACK Service & ARP Ping")
        self.assertEqual(ct, AliveTest.ICMP_TCP_ACK_SERVICE_AND_ARP_PING)

    def test_consider_alive(self):
        ct = AliveTest.from_string("Consider Alive")
        self.assertEqual(ct, AliveTest.CONSIDER_ALIVE)


if __name__ == "__main__":
    unittest.main()
