# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import (
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)


class GetSnmpAuthAlgorithmFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            SnmpAuthAlgorithm.from_string("foo")

    def test_none_or_empty_type(self):
        ts = SnmpAuthAlgorithm.from_string(None)
        self.assertIsNone(ts)
        ts = SnmpAuthAlgorithm.from_string("")
        self.assertIsNone(ts)

    def test_sha1(self):
        ts = SnmpAuthAlgorithm.from_string("sha1")
        self.assertEqual(ts, SnmpAuthAlgorithm.SHA1)

    def test_md5(self):
        ts = SnmpAuthAlgorithm.from_string("md5")
        self.assertEqual(ts, SnmpAuthAlgorithm.MD5)


class GetSnmpPrivacyAlgorithmFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            SnmpPrivacyAlgorithm.from_string("foo")

    def test_none_or_empty_type(self):
        ts = SnmpPrivacyAlgorithm.from_string(None)
        self.assertIsNone(ts)
        ts = SnmpPrivacyAlgorithm.from_string("")
        self.assertIsNone(ts)

    def test_aes(self):
        ts = SnmpPrivacyAlgorithm.from_string("aes")
        self.assertEqual(ts, SnmpPrivacyAlgorithm.AES)

    def test_des(self):
        ts = SnmpPrivacyAlgorithm.from_string("des")
        self.assertEqual(ts, SnmpPrivacyAlgorithm.DES)
