# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v227 import HostsOrdering


class GetHostsOrderingFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            HostsOrdering.from_string("foo")

    def test_none_or_empty(self):
        ct = HostsOrdering.from_string(None)
        self.assertIsNone(ct)
        ct = HostsOrdering.from_string("")
        self.assertIsNone(ct)

    def test_sequential(self):
        ct = HostsOrdering.from_string("sequential")
        self.assertEqual(ct, HostsOrdering.SEQUENTIAL)

    def test_random(self):
        ct = HostsOrdering.from_string("random")
        self.assertEqual(ct, HostsOrdering.RANDOM)

    def test_reverse(self):
        ct = HostsOrdering.from_string("reverse")
        self.assertEqual(ct, HostsOrdering.REVERSE)
