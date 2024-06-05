# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import SystemReports


class SystemReportsTestCase(unittest.TestCase):
    def test_get_system_reports(self):
        request = SystemReports.get_system_reports()

        self.assertEqual(bytes(request), b"<get_system_reports/>")

    def test_system_reports_with_name(self):
        request = SystemReports.get_system_reports(name="foo")

        self.assertEqual(bytes(request), b'<get_system_reports name="foo"/>')

    def test_system_reports_with_slave_id(self):
        request = SystemReports.get_system_reports(slave_id="s1")

        self.assertEqual(bytes(request), b'<get_system_reports slave_id="s1"/>')

    def test_system_reports_with_brief(self):
        request = SystemReports.get_system_reports(brief=True)

        self.assertEqual(bytes(request), b'<get_system_reports brief="1"/>')

        request = SystemReports.get_system_reports(brief=False)

        self.assertEqual(bytes(request), b'<get_system_reports brief="0"/>')

    def test_system_reports_with_duration(self):
        request = SystemReports.get_system_reports(duration=3600)

        self.assertEqual(
            bytes(request), b'<get_system_reports duration="3600"/>'
        )

    def test_system_reports_with_invalid_duration(self):
        with self.assertRaises(InvalidArgument):
            SystemReports.get_system_reports(duration="")

    def test_system_reports_with_start_time(self):
        request = SystemReports.get_system_reports(start_time="01-01-2019")

        self.assertEqual(
            bytes(request), b'<get_system_reports start_time="01-01-2019"/>'
        )

    def test_system_reports_with_end_time(self):
        request = SystemReports.get_system_reports(end_time="01-01-2019")

        self.assertEqual(
            bytes(request), b'<get_system_reports end_time="01-01-2019"/>'
        )
