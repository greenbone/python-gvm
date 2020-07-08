# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
from gvm.protocols.gmpv208 import AlertMethod, get_alert_method_from_string


class GetAlertMethodFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_alert_method_from_string('foo')

    def test_none_or_empty(self):
        ct = get_alert_method_from_string(None)
        self.assertIsNone(ct)
        ct = get_alert_method_from_string('')
        self.assertIsNone(ct)

    def test_email(self):
        ct = get_alert_method_from_string('email')
        self.assertEqual(ct, AlertMethod.EMAIL)

    def test_scp(self):
        ct = get_alert_method_from_string('scp')
        self.assertEqual(ct, AlertMethod.SCP)

    def test_send(self):
        ct = get_alert_method_from_string('send')
        self.assertEqual(ct, AlertMethod.SEND)

    def test_smb(self):
        ct = get_alert_method_from_string('smb')
        self.assertEqual(ct, AlertMethod.SMB)

    def test_snmp(self):
        ct = get_alert_method_from_string('snmp')
        self.assertEqual(ct, AlertMethod.SNMP)

    def test_syslog(self):
        ct = get_alert_method_from_string('syslog')
        self.assertEqual(ct, AlertMethod.SYSLOG)

    def test_http_get(self):
        ct = get_alert_method_from_string('HTTP Get')
        self.assertEqual(ct, AlertMethod.HTTP_GET)

    def test_start_task(self):
        ct = get_alert_method_from_string('Start Task')
        self.assertEqual(ct, AlertMethod.START_TASK)

    def test_sourcefire_connector(self):
        ct = get_alert_method_from_string('sourcefire Connector')
        self.assertEqual(ct, AlertMethod.SOURCEFIRE_CONNECTOR)

    def test_verinice_connector(self):
        ct = get_alert_method_from_string('verinice Connector')
        self.assertEqual(ct, AlertMethod.VERINICE_CONNECTOR)


if __name__ == '__main__':
    unittest.main()
