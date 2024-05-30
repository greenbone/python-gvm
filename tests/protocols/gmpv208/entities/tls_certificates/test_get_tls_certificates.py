# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetTLSCertificatesTestMixin:
    def test_get_tls_certificates(self):
        self.gmp.get_tls_certificates()

        self.connection.send.has_been_called_with(b"<get_tls_certificates/>")

    def test_get_tls_certificates_with_filter_string(self):
        self.gmp.get_tls_certificates(filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_tls_certificates filter="name=foo"/>'
        )

    def test_get_tls_certificates_with_include_certificate_data(self):
        self.gmp.get_tls_certificates(include_certificate_data="1")

        self.connection.send.has_been_called_with(
            b'<get_tls_certificates include_certificate_data="1"/>'
        )

    def test_get_tls_certificates_with_details(self):
        self.gmp.get_tls_certificates(details="1")

        self.connection.send.has_been_called_with(
            b'<get_tls_certificates details="1"/>'
        )
