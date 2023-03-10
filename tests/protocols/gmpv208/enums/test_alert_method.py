# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Greenbone AG
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
from gvm.protocols.gmpv208 import AlertMethod


class GetAlertMethodFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            AlertMethod.from_string("foo")

    def test_none_or_empty(self):
        ct = AlertMethod.from_string(None)
        self.assertIsNone(ct)
        ct = AlertMethod.from_string("")
        self.assertIsNone(ct)

    def test_email(self):
        ct = AlertMethod.from_string("email")
        self.assertEqual(ct, AlertMethod.EMAIL)

    def test_scp(self):
        ct = AlertMethod.from_string("scp")
        self.assertEqual(ct, AlertMethod.SCP)

    def test_send(self):
        ct = AlertMethod.from_string("send")
        self.assertEqual(ct, AlertMethod.SEND)

    def test_smb(self):
        ct = AlertMethod.from_string("smb")
        self.assertEqual(ct, AlertMethod.SMB)

    def test_snmp(self):
        ct = AlertMethod.from_string("snmp")
        self.assertEqual(ct, AlertMethod.SNMP)

    def test_syslog(self):
        ct = AlertMethod.from_string("syslog")
        self.assertEqual(ct, AlertMethod.SYSLOG)

    def test_http_get(self):
        ct = AlertMethod.from_string("HTTP Get")
        self.assertEqual(ct, AlertMethod.HTTP_GET)

    def test_start_task(self):
        ct = AlertMethod.from_string("Start Task")
        self.assertEqual(ct, AlertMethod.START_TASK)

    def test_sourcefire_connector(self):
        ct = AlertMethod.from_string("sourcefire Connector")
        self.assertEqual(ct, AlertMethod.SOURCEFIRE_CONNECTOR)

    def test_verinice_connector(self):
        ct = AlertMethod.from_string("verinice Connector")
        self.assertEqual(ct, AlertMethod.VERINICE_CONNECTOR)

    def test_tippingpoint_sms(self):
        ct = AlertMethod.from_string("Tippingpoint SMS")
        self.assertEqual(ct, AlertMethod.TIPPINGPOINT_SMS)

    def test_alemba_vfire(self):
        ct = AlertMethod.from_string("Alemba vFire")
        self.assertEqual(ct, AlertMethod.ALEMBA_VFIRE)


if __name__ == "__main__":
    unittest.main()
