# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetCveListTestMixin:
    def test_get_cpes(self):
        self.gmp.get_cves()

        self.connection.send.has_been_called_with(b'<get_info type="CVE"/>')

    def test_get_cves_with_filter_string(self):
        self.gmp.get_cves(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="CVE" filter="foo=bar"/>'
        )

    def test_get_cves_with_filter_id(self):
        self.gmp.get_cves(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="CVE" filt_id="f1"/>'
        )

    def test_get_cves_with_name(self):
        self.gmp.get_cves(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="CVE" name="foo"/>'
        )

    def test_get_cves_with_details(self):
        self.gmp.get_cves(details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="CVE" details="1"/>'
        )

        self.gmp.get_cves(details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="CVE" details="0"/>'
        )
