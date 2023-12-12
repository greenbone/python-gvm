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
from gvm.protocols.gmpv225 import ResourceType


class GetResourceTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ResourceType.from_string("foo")

    def test_none_or_empty(self):
        ct = ResourceType.from_string(None)
        self.assertIsNone(ct)
        ct = ResourceType.from_string("")
        self.assertIsNone(ct)

    def test_alert(self):
        ct = ResourceType.from_string("alert")
        self.assertEqual(ct, ResourceType.ALERT)

    def test_cert_bund_adv(self):
        ct = ResourceType.from_string("cert_bund_adv")
        self.assertEqual(ct, ResourceType.CERT_BUND_ADV)

    def test_config(self):
        ct = ResourceType.from_string("config")
        self.assertEqual(ct, ResourceType.CONFIG)

    def test_cpe(self):
        ct = ResourceType.from_string("cpe")
        self.assertEqual(ct, ResourceType.CPE)

    def test_credential(self):
        ct = ResourceType.from_string("credential")
        self.assertEqual(ct, ResourceType.CREDENTIAL)

    def test_cve(self):
        ct = ResourceType.from_string("cve")
        self.assertEqual(ct, ResourceType.CVE)

    def test_dfn_cert_adv(self):
        ct = ResourceType.from_string("dfn_cert_adv")
        self.assertEqual(ct, ResourceType.DFN_CERT_ADV)

    def test_filter(self):
        ct = ResourceType.from_string("filter")
        self.assertEqual(ct, ResourceType.FILTER)

    def test_group(self):
        ct = ResourceType.from_string("group")
        self.assertEqual(ct, ResourceType.GROUP)

    def test_host(self):
        ct = ResourceType.from_string("host")
        self.assertEqual(ct, ResourceType.HOST)

    def test_note(self):
        ct = ResourceType.from_string("note")
        self.assertEqual(ct, ResourceType.NOTE)

    def test_nvt(self):
        ct = ResourceType.from_string("nvt")
        self.assertEqual(ct, ResourceType.NVT)

    def test_os(self):
        ct = ResourceType.from_string("os")
        self.assertEqual(ct, ResourceType.OS)

    def test_override(self):
        ct = ResourceType.from_string("override")
        self.assertEqual(ct, ResourceType.OVERRIDE)

    def test_permission(self):
        ct = ResourceType.from_string("permission")
        self.assertEqual(ct, ResourceType.PERMISSION)

    def test_port_list(self):
        ct = ResourceType.from_string("port_list")
        self.assertEqual(ct, ResourceType.PORT_LIST)

    def test_report_format(self):
        ct = ResourceType.from_string("report_format")
        self.assertEqual(ct, ResourceType.REPORT_FORMAT)

    def test_report(self):
        ct = ResourceType.from_string("report")
        self.assertEqual(ct, ResourceType.REPORT)

    def test_result(self):
        ct = ResourceType.from_string("result")
        self.assertEqual(ct, ResourceType.RESULT)

    def test_role(self):
        ct = ResourceType.from_string("role")
        self.assertEqual(ct, ResourceType.ROLE)

    def test_scanner(self):
        ct = ResourceType.from_string("scanner")
        self.assertEqual(ct, ResourceType.SCANNER)

    def test_schedule(self):
        ct = ResourceType.from_string("schedule")
        self.assertEqual(ct, ResourceType.SCHEDULE)

    def test_target(self):
        ct = ResourceType.from_string("target")
        self.assertEqual(ct, ResourceType.TARGET)

    def test_task(self):
        ct = ResourceType.from_string("task")
        self.assertEqual(ct, ResourceType.TASK)

    def test_tls_certificate(self):
        ct = ResourceType.from_string("tls_certificate")
        self.assertEqual(ct, ResourceType.TLS_CERTIFICATE)

    def test_user(self):
        ct = ResourceType.from_string("user")
        self.assertEqual(ct, ResourceType.USER)

    def test_allresources(self):
        with self.assertRaises(InvalidArgument):
            ResourceType.from_string("allresources")


if __name__ == "__main__":
    unittest.main()
