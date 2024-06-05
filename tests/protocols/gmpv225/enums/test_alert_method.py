# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v225 import AlertMethod


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
