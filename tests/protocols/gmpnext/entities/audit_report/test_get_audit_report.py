# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetAuditReportTestMixin:
    def test_get_audit_report_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_audit_report(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_audit_report("")

    def test_get_audit_report_with_id(self):
        self.gmp.get_audit_report(audit_report_id="r1")

        self.connection.send.has_been_called_with(
            b'<get_audit_report audit_report_id="r1"/>'
        )

    def test_get_audit_report_with_filter_string(self):
        self.gmp.get_audit_report(
            audit_report_id="r1",
            filter_string="name=foo",
        )

        self.connection.send.has_been_called_with(
            b'<get_audit_report audit_report_id="r1" filter="name=foo"/>'
        )

    def test_get_audit_report_with_filter_id(self):
        self.gmp.get_audit_report(
            audit_report_id="r1",
            filter_id="f1",
        )

        self.connection.send.has_been_called_with(
            b'<get_audit_report audit_report_id="r1" filt_id="f1"/>'
        )

    def test_get_audit_report_with_filter_string_and_filter_id(self):
        self.gmp.get_audit_report(
            audit_report_id="r1",
            filter_string="name=foo",
            filter_id="f1",
        )

        self.connection.send.has_been_called_with(
            b'<get_audit_report audit_report_id="r1" '
            b'filter="name=foo" filt_id="f1"/>'
        )
