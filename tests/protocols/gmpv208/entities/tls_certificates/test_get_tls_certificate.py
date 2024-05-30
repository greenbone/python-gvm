# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpGetTLSCertificateTestMixin:
    def test_get_tls_certificate(self):
        self.gmp.get_tls_certificate("t1")

        self.connection.send.has_been_called_with(
            b'<get_tls_certificates tls_certificate_id="t1" '
            b'include_certificate_data="1" details="1"/>'
        )

    def test_fail_without_tls_certificate_id(self):
        with self.assertRaises(GvmError):
            self.gmp.get_tls_certificate(None)

        with self.assertRaises(GvmError):
            self.gmp.get_tls_certificate("")
