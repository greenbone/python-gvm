# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetReportClosedCVEsTestMixin:
    def test_get_report_closed_cves_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_closed_cves(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_closed_cves("")

    def test_get_report_closed_cves_with_ignore_pagination(self):
        self.gmp.get_report_closed_cves(report_id="r1", ignore_pagination=True)

        self.connection.send.has_been_called_with(
            b'<get_report_closed_cves report_id="r1" ignore_pagination="1" details="1"/>'
        )

        self.gmp.get_report_closed_cves(report_id="r1", ignore_pagination=False)

        self.connection.send.has_been_called_with(
            b'<get_report_closed_cves report_id="r1" ignore_pagination="0" details="1"/>'
        )

    def test_get_report_closed_cves_with_details(self):
        self.gmp.get_report_closed_cves(report_id="r1", details=True)

        self.connection.send.has_been_called_with(
            b'<get_report_closed_cves report_id="r1" details="1"/>'
        )

        self.gmp.get_report_closed_cves(report_id="r1", details=False)

        self.connection.send.has_been_called_with(
            b'<get_report_closed_cves report_id="r1" details="0"/>'
        )
