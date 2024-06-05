# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import FeedType


class GetFeedTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            FeedType.from_string("foo")

    def test_none_or_empty(self):
        ct = FeedType.from_string(None)
        self.assertIsNone(ct)
        ct = FeedType.from_string("")
        self.assertIsNone(ct)

    def test_nvt(self):
        ct = FeedType.from_string("nvt")
        self.assertEqual(ct, FeedType.NVT)

    def test_cert(self):
        ct = FeedType.from_string("cert")
        self.assertEqual(ct, FeedType.CERT)

    def test_scap(self):
        ct = FeedType.from_string("scap")
        self.assertEqual(ct, FeedType.SCAP)

    def test_gvmd_data(self):
        ct = FeedType.from_string("gvmd_data")
        self.assertEqual(ct, FeedType.GVMD_DATA)


if __name__ == "__main__":
    unittest.main()
