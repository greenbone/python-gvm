# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetReportFormatsTestMixin:
    def test_get_report_formats(self):
        self.gmp.get_report_formats()

        self.connection.send.has_been_called_with(b"<get_report_formats/>")

    def test_get_report_formats_with_filter_string(self):
        self.gmp.get_report_formats(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_report_formats filter="foo=bar"/>'
        )

    def test_get_report_formats_with_filter_id(self):
        self.gmp.get_report_formats(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_report_formats filt_id="f1"/>'
        )

    def test_get_report_formats_with_trash(self):
        self.gmp.get_report_formats(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_report_formats trash="1"/>'
        )

        self.gmp.get_report_formats(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_report_formats trash="0"/>'
        )

    def test_get_report_formats_with_details(self):
        self.gmp.get_report_formats(details=True)

        self.connection.send.has_been_called_with(
            b'<get_report_formats details="1"/>'
        )

        self.gmp.get_report_formats(details=False)

        self.connection.send.has_been_called_with(
            b'<get_report_formats details="0"/>'
        )

    def test_get_report_formats_with_alerts(self):
        self.gmp.get_report_formats(alerts=True)

        self.connection.send.has_been_called_with(
            b'<get_report_formats alerts="1"/>'
        )

        self.gmp.get_report_formats(alerts=False)

        self.connection.send.has_been_called_with(
            b'<get_report_formats alerts="0"/>'
        )

    def test_get_report_formats_with_params(self):
        self.gmp.get_report_formats(params=True)

        self.connection.send.has_been_called_with(
            b'<get_report_formats params="1"/>'
        )

        self.gmp.get_report_formats(params=False)

        self.connection.send.has_been_called_with(
            b'<get_report_formats params="0"/>'
        )
