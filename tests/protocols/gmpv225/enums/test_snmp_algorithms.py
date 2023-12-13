# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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
from gvm.protocols.gmpv225 import SnmpAuthAlgorithm, SnmpPrivacyAlgorithm


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
