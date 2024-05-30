# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetReportsTestMixin:
    def test_get_reports(self):
        self.gmp.get_reports()

        self.connection.send.has_been_called_with(b"<get_reports/>")

    def test_get_reports_with_filter_string(self):
        self.gmp.get_reports(filter_string="name=foo", ignore_pagination=1)

        self.connection.send.has_been_called_with(
            b'<get_reports report_filter="name=foo" ignore_pagination="1"/>'
        )

    def test_get_reports_with_filter_id(self):
        self.gmp.get_reports(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_reports report_filt_id="f1"/>'
        )

    def test_get_reports_without_note_details(self):
        self.gmp.get_reports(note_details=False)

        self.connection.send.has_been_called_with(
            b'<get_reports note_details="0"/>'
        )

    def test_get_reports_with_note_details(self):
        self.gmp.get_reports(note_details=True, ignore_pagination=False)

        self.connection.send.has_been_called_with(
            b'<get_reports note_details="1" ignore_pagination="0"/>'
        )

    def test_get_reports_without_override_details(self):
        self.gmp.get_reports(override_details=False)

        self.connection.send.has_been_called_with(
            b'<get_reports override_details="0"/>'
        )

    def test_get_reports_with_override_details(self):
        self.gmp.get_reports(override_details=True)

        self.connection.send.has_been_called_with(
            b'<get_reports override_details="1"/>'
        )

    def test_get_reports_with_details(self):
        self.gmp.get_reports(details=True)

        self.connection.send.has_been_called_with(b'<get_reports details="1"/>')

    def test_get_reports_without_details(self):
        self.gmp.get_reports(details=False)

        self.connection.send.has_been_called_with(b'<get_reports details="0"/>')
