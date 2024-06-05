# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyTLSCertificateTestMixin:
    def test_modify_tls_certificate(self):
        self.gmp.modify_tls_certificate("c1")

        self.connection.send.has_been_called_with(
            b'<modify_tls_certificate tls_certificate_id="c1"/>'
        )

    def test_modify_tls_certificate_with_name(self):
        self.gmp.modify_tls_certificate("c1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_tls_certificate tls_certificate_id="c1">'
            b"<name>foo</name>"
            b"</modify_tls_certificate>"
        )

    def test_modify_tls_certificate_with_comment(self):
        self.gmp.modify_tls_certificate("c1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_tls_certificate tls_certificate_id="c1">'
            b"<comment>foo</comment>"
            b"</modify_tls_certificate>"
        )

    def test_modify_tls_certificate_with_trust(self):
        self.gmp.modify_tls_certificate("c1", trust=True)

        self.connection.send.has_been_called_with(
            b'<modify_tls_certificate tls_certificate_id="c1">'
            b"<trust>1</trust>"
            b"</modify_tls_certificate>"
        )

        self.gmp.modify_tls_certificate("c1", trust=False)

        self.connection.send.has_been_called_with(
            b'<modify_tls_certificate tls_certificate_id="c1">'
            b"<trust>0</trust>"
            b"</modify_tls_certificate>"
        )

    def test_missing_tls_certificate_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tls_certificate(name="foo", tls_certificate_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tls_certificate(name="foo", tls_certificate_id=None)
