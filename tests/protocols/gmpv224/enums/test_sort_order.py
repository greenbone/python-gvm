# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import SortOrder


class GetSortOrderFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            SortOrder.from_string("foo")

    def test_none_or_empty(self):
        ct = SortOrder.from_string(None)
        self.assertIsNone(ct)
        ct = SortOrder.from_string("")
        self.assertIsNone(ct)

    def test_ascending(self):
        ct = SortOrder.from_string("ascending")
        self.assertEqual(ct, SortOrder.ASCENDING)

    def test_descending(self):
        ct = SortOrder.from_string("descending")
        self.assertEqual(ct, SortOrder.DESCENDING)


if __name__ == "__main__":
    unittest.main()
