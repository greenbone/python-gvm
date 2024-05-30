# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetDfnCertListTestMixin:
    def test_get_cpes(self):
        self.gmp.get_dfn_cert_advisories()

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV"/>'
        )

    def test_get_cves_with_filter_string(self):
        self.gmp.get_dfn_cert_advisories(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV" filter="foo=bar"/>'
        )

    def test_get_cves_with_filter_id(self):
        self.gmp.get_dfn_cert_advisories(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV" filt_id="f1"/>'
        )

    def test_get_cves_with_name(self):
        self.gmp.get_dfn_cert_advisories(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV" name="foo"/>'
        )

    def test_get_cves_with_details(self):
        self.gmp.get_dfn_cert_advisories(details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV" details="1"/>'
        )

        self.gmp.get_dfn_cert_advisories(details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV" details="0"/>'
        )
