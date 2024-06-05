# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import PortRangeType


class GetPortRangeTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            PortRangeType.from_string("foo")

    def test_none_or_empty(self):
        ct = PortRangeType.from_string(None)
        self.assertIsNone(ct)
        ct = PortRangeType.from_string("")
        self.assertIsNone(ct)

    def test_tcp(self):
        ct = PortRangeType.from_string("tcp")
        self.assertEqual(ct, PortRangeType.TCP)

    def test_udp(self):
        ct = PortRangeType.from_string("udp")
        self.assertEqual(ct, PortRangeType.UDP)


if __name__ == "__main__":
    unittest.main()
