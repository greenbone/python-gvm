# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteTLSCertificateTestMixin:
    def test_delete(self):
        self.gmp.delete_tls_certificate("a1")

        self.connection.send.has_been_called_with(
            b'<delete_tls_certificate tls_certificate_id="a1"/>'
        )

    def test_delete_ultimate(self):
        with self.assertRaises(TypeError):
            self.gmp.delete_tls_certificate("a1", ultimate=True)

    def test_missing_tls_certificate_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_tls_certificate(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_tls_certificate("")
