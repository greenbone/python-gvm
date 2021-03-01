# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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
from gvm.protocols.gmpv208 import (
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
)


class GetSnmpAuthAlgorithmFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            get_snmp_auth_algorithm_from_string('foo')

    def test_none_or_empty_type(self):
        ts = get_snmp_auth_algorithm_from_string(None)
        self.assertIsNone(ts)
        ts = get_snmp_auth_algorithm_from_string('')
        self.assertIsNone(ts)

    def test_sha1(self):
        ts = get_snmp_auth_algorithm_from_string('sha1')
        self.assertEqual(ts, SnmpAuthAlgorithm.SHA1)

    def test_md5(self):
        ts = get_snmp_auth_algorithm_from_string('md5')
        self.assertEqual(ts, SnmpAuthAlgorithm.MD5)


class GetSnmpPrivacyAlgorithmFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            get_snmp_privacy_algorithm_from_string('foo')

    def test_none_or_empty_type(self):
        ts = get_snmp_privacy_algorithm_from_string(None)
        self.assertIsNone(ts)
        ts = get_snmp_privacy_algorithm_from_string('')
        self.assertIsNone(ts)

    def test_aes(self):
        ts = get_snmp_privacy_algorithm_from_string('aes')
        self.assertEqual(ts, SnmpPrivacyAlgorithm.AES)

    def test_des(self):
        ts = get_snmp_privacy_algorithm_from_string('des')
        self.assertEqual(ts, SnmpPrivacyAlgorithm.DES)
