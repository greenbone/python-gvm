# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import EntityType


class GetEntityTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            EntityType.from_string("foo")

    def test_none_or_empty(self):
        ct = EntityType.from_string(None)
        self.assertIsNone(ct)
        ct = EntityType.from_string("")
        self.assertIsNone(ct)

    def test_audit(self):
        ct = EntityType.from_string("audit")
        self.assertEqual(ct, EntityType.AUDIT)

    def test_alert(self):
        ct = EntityType.from_string("alert")
        self.assertEqual(ct, EntityType.ALERT)

    def test_asset(self):
        ct = EntityType.from_string("asset")
        self.assertEqual(ct, EntityType.ASSET)

    def test_cert_bund_adv(self):
        ct = EntityType.from_string("cert_bund_adv")
        self.assertEqual(ct, EntityType.CERT_BUND_ADV)

    def test_cpe(self):
        ct = EntityType.from_string("cpe")
        self.assertEqual(ct, EntityType.CPE)

    def test_credential(self):
        ct = EntityType.from_string("credential")
        self.assertEqual(ct, EntityType.CREDENTIAL)

    def test_dfn_cert_adv(self):
        ct = EntityType.from_string("dfn_cert_adv")
        self.assertEqual(ct, EntityType.DFN_CERT_ADV)

    def test_filter(self):
        ct = EntityType.from_string("filter")
        self.assertEqual(ct, EntityType.FILTER)

    def test_group(self):
        ct = EntityType.from_string("group")
        self.assertEqual(ct, EntityType.GROUP)

    def test_host(self):
        ct = EntityType.from_string("host")
        self.assertEqual(ct, EntityType.HOST)

    def test_info(self):
        ct = EntityType.from_string("info")
        self.assertEqual(ct, EntityType.INFO)

    def test_note(self):
        ct = EntityType.from_string("note")
        self.assertEqual(ct, EntityType.NOTE)

    def test_nvt(self):
        ct = EntityType.from_string("nvt")
        self.assertEqual(ct, EntityType.NVT)

    def test_operating_system(self):
        ct = EntityType.from_string("os")
        self.assertEqual(ct, EntityType.OPERATING_SYSTEM)

        ct = EntityType.from_string("operating_system")
        self.assertEqual(ct, EntityType.OPERATING_SYSTEM)

    def test_ovaldef(self):
        ct = EntityType.from_string("ovaldef")
        self.assertEqual(ct, EntityType.OVALDEF)

    def test_override(self):
        ct = EntityType.from_string("override")
        self.assertEqual(ct, EntityType.OVERRIDE)

    def test_permission(self):
        ct = EntityType.from_string("permission")
        self.assertEqual(ct, EntityType.PERMISSION)

    def test_policy(self):
        ct = EntityType.from_string("policy")
        self.assertEqual(ct, EntityType.POLICY)

    def test_port_list(self):
        ct = EntityType.from_string("port_list")
        self.assertEqual(ct, EntityType.PORT_LIST)

    def test_report(self):
        ct = EntityType.from_string("report")
        self.assertEqual(ct, EntityType.REPORT)

    def test_report_format(self):
        ct = EntityType.from_string("report_format")
        self.assertEqual(ct, EntityType.REPORT_FORMAT)

    def test_result(self):
        ct = EntityType.from_string("result")
        self.assertEqual(ct, EntityType.RESULT)

    def test_role(self):
        ct = EntityType.from_string("role")
        self.assertEqual(ct, EntityType.ROLE)

    def test_scan_config(self):
        ct = EntityType.from_string("config")
        self.assertEqual(ct, EntityType.SCAN_CONFIG)

        ct = EntityType.from_string("scan_config")
        self.assertEqual(ct, EntityType.SCAN_CONFIG)

    def test_scanner(self):
        ct = EntityType.from_string("scanner")
        self.assertEqual(ct, EntityType.SCANNER)

    def test_schedule(self):
        ct = EntityType.from_string("schedule")
        self.assertEqual(ct, EntityType.SCHEDULE)

    def test_tag(self):
        ct = EntityType.from_string("tag")
        self.assertEqual(ct, EntityType.TAG)

    def test_target(self):
        ct = EntityType.from_string("target")
        self.assertEqual(ct, EntityType.TARGET)

    def test_task(self):
        ct = EntityType.from_string("task")
        self.assertEqual(ct, EntityType.TASK)

    def test_ticket(self):
        ct = EntityType.from_string("ticket")
        self.assertEqual(ct, EntityType.TICKET)

    def test_tls_certificate(self):
        ft = EntityType.from_string("tls_certificate")
        self.assertEqual(ft, EntityType.TLS_CERTIFICATE)

    def test_user(self):
        ct = EntityType.from_string("user")
        self.assertEqual(ct, EntityType.USER)

    def test_vulnerability(self):
        ct = EntityType.from_string("vuln")
        self.assertEqual(ct, EntityType.VULNERABILITY)

        ct = EntityType.from_string("vulnerability")
        self.assertEqual(ct, EntityType.VULNERABILITY)


if __name__ == "__main__":
    unittest.main()
