# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneTLSCertificateTestMixin:
    def test_clone(self):
        self.gmp.clone_tls_certificate("a1")

        self.connection.send.has_been_called_with(
            b"<create_tls_certificate>"
            b"<copy>a1</copy>"
            b"</create_tls_certificate>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_tls_certificate("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_tls_certificate(None)
