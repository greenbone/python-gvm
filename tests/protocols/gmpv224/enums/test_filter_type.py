# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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
from gvm.protocols.gmpv224 import FilterType


class GetFilterTypeFomStringTestCase(unittest.TestCase):
    def test_filter_type_alert(self):
        ft = FilterType.from_string("alert")
        self.assertEqual(ft, FilterType.ALERT)

    def test_filter_type_asset(self):
        ft = FilterType.from_string("asset")
        self.assertEqual(ft, FilterType.ASSET)

    def test_filter_type_credential(self):
        ft = FilterType.from_string("credential")
        self.assertEqual(ft, FilterType.CREDENTIAL)

    def test_filter_type_filter(self):
        ft = FilterType.from_string("filter")
        self.assertEqual(ft, FilterType.FILTER)

    def test_filter_type_group(self):
        ft = FilterType.from_string("group")
        self.assertEqual(ft, FilterType.GROUP)

    def test_filter_type_host(self):
        ft = FilterType.from_string("host")
        self.assertEqual(ft, FilterType.HOST)

    def test_filter_type_note(self):
        ft = FilterType.from_string("note")
        self.assertEqual(ft, FilterType.NOTE)

    def test_filter_type_override(self):
        ft = FilterType.from_string("override")
        self.assertEqual(ft, FilterType.OVERRIDE)

    def test_filter_type_permission(self):
        ft = FilterType.from_string("permission")
        self.assertEqual(ft, FilterType.PERMISSION)

    def test_filter_type_port_list(self):
        ft = FilterType.from_string("port_list")
        self.assertEqual(ft, FilterType.PORT_LIST)

    def test_filter_type_report(self):
        ft = FilterType.from_string("report")
        self.assertEqual(ft, FilterType.REPORT)

    def test_filter_type_report_format(self):
        ft = FilterType.from_string("report_format")
        self.assertEqual(ft, FilterType.REPORT_FORMAT)

    def test_filter_type_result(self):
        ft = FilterType.from_string("result")
        self.assertEqual(ft, FilterType.RESULT)

    def test_filter_type_role(self):
        ft = FilterType.from_string("role")
        self.assertEqual(ft, FilterType.ROLE)

    def test_filter_type_schedule(self):
        ft = FilterType.from_string("schedule")
        self.assertEqual(ft, FilterType.SCHEDULE)

    def test_filter_type_secinfo(self):
        ft = FilterType.from_string("secinfo")
        self.assertEqual(ft, FilterType.ALL_SECINFO)

    def test_filter_type_all_secinfo(self):
        ft = FilterType.from_string("all_secinfo")
        self.assertEqual(ft, FilterType.ALL_SECINFO)

    def test_filter_type_tag(self):
        ft = FilterType.from_string("tag")
        self.assertEqual(ft, FilterType.TAG)

    def test_filter_type_task(self):
        ft = FilterType.from_string("task")
        self.assertEqual(ft, FilterType.TASK)

    def test_filter_type_target(self):
        ft = FilterType.from_string("target")
        self.assertEqual(ft, FilterType.TARGET)

    def test_filter_type_ticket(self):
        ft = FilterType.from_string("ticket")
        self.assertEqual(ft, FilterType.TICKET)

    def test_filter_type_tls_certificate(self):
        ft = FilterType.from_string("tls_certificate")
        self.assertEqual(ft, FilterType.TLS_CERTIFICATE)

    def test_filter_type_operating_system(self):
        ft = FilterType.from_string("operating_system")
        self.assertEqual(ft, FilterType.OPERATING_SYSTEM)

    def test_filter_type_user(self):
        ft = FilterType.from_string("user")
        self.assertEqual(ft, FilterType.USER)

    def test_filter_type_vuln(self):
        ft = FilterType.from_string("vuln")
        self.assertEqual(ft, FilterType.VULNERABILITY)

    def test_filter_type_vulnerability(self):
        ft = FilterType.from_string("vulnerability")
        self.assertEqual(ft, FilterType.VULNERABILITY)

    def test_filter_type_config(self):
        ft = FilterType.from_string("config")
        self.assertEqual(ft, FilterType.SCAN_CONFIG)

    def test_filter_type_scan_config(self):
        ft = FilterType.from_string("scan_config")
        self.assertEqual(ft, FilterType.SCAN_CONFIG)

    def test_filter_type_os(self):
        ft = FilterType.from_string("os")
        self.assertEqual(ft, FilterType.OPERATING_SYSTEM)

    def test_invalid_filter_type(self):
        with self.assertRaises(InvalidArgument):
            FilterType.from_string("foo")

    def test_non_or_empty_filter_type(self):
        ft = FilterType.from_string(None)
        self.assertIsNone(ft)

        ft = FilterType.from_string("")
        self.assertIsNone(ft)
