# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.protocols.gmp.requests.v226 import FilterType


class FilterTypeTestsCase(unittest.TestCase):
    def test_filter_type_all_secinfo(self):
        self.assertEqual(FilterType.ALL_SECINFO.value, "secinfo")

    def test_filter_type_alert(self):
        self.assertEqual(FilterType.ALERT.value, "alert")

    def test_filter_type_audit_report(self):
        self.assertEqual(FilterType.AUDIT_REPORT.value, "audit_report")

    def test_filter_type_asset(self):
        self.assertEqual(FilterType.ASSET.value, "asset")

    def test_filter_type_credential(self):
        self.assertEqual(FilterType.CREDENTIAL.value, "credential")

    def test_filter_type_filter(self):
        self.assertEqual(FilterType.FILTER.value, "filter")

    def test_filter_type_group(self):
        self.assertEqual(FilterType.GROUP.value, "group")

    def test_filter_type_host(self):
        self.assertEqual(FilterType.HOST.value, "host")

    def test_filter_type_note(self):
        self.assertEqual(FilterType.NOTE.value, "note")

    def test_filter_type_operating_system(self):
        self.assertEqual(FilterType.OPERATING_SYSTEM.value, "os")

    def test_filter_type_override(self):
        self.assertEqual(FilterType.OVERRIDE.value, "override")

    def test_filter_type_permission(self):
        self.assertEqual(FilterType.PERMISSION.value, "permission")

    def test_filter_type_port_list(self):
        self.assertEqual(FilterType.PORT_LIST.value, "port_list")

    def test_filter_type_report(self):
        self.assertEqual(FilterType.REPORT.value, "report")

    def test_filter_type_report_config(self):
        self.assertEqual(FilterType.REPORT_CONFIG.value, "report_config")

    def test_filter_type_report_format(self):
        self.assertEqual(FilterType.REPORT_FORMAT.value, "report_format")

    def test_filter_type_result(self):
        self.assertEqual(FilterType.RESULT.value, "result")

    def test_filter_type_role(self):
        self.assertEqual(FilterType.ROLE.value, "role")

    def test_filter_type_scan_config(self):
        self.assertEqual(FilterType.SCAN_CONFIG.value, "config")

    def test_filter_type_schedule(self):
        self.assertEqual(FilterType.SCHEDULE.value, "schedule")

    def test_filter_type_tag(self):
        self.assertEqual(FilterType.TAG.value, "tag")

    def test_filter_type_target(self):
        self.assertEqual(FilterType.TARGET.value, "target")

    def test_filter_type_task(self):
        self.assertEqual(FilterType.TASK.value, "task")

    def test_filter_type_ticket(self):
        self.assertEqual(FilterType.TICKET.value, "ticket")

    def test_filter_type_tls_certificate(self):
        self.assertEqual(FilterType.TLS_CERTIFICATE.value, "tls_certificate")

    def test_filter_type_user(self):
        self.assertEqual(FilterType.USER.value, "user")

    def test_filter_type_vulnerability(self):
        self.assertEqual(FilterType.VULNERABILITY.value, "vuln")

    def test_filter_type_from_string_vuln(self):
        self.assertEqual(
            FilterType.from_string("vuln"), FilterType.VULNERABILITY
        )

    def test_filter_type_from_string_os(self):
        self.assertEqual(
            FilterType.from_string("os"), FilterType.OPERATING_SYSTEM
        )

    def test_filter_type_from_string_config(self):
        self.assertEqual(
            FilterType.from_string("config"), FilterType.SCAN_CONFIG
        )

    def test_filter_type_from_string_secinfo(self):
        self.assertEqual(
            FilterType.from_string("secinfo"), FilterType.ALL_SECINFO
        )
