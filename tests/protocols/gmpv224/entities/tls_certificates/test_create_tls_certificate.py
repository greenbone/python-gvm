# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateTLSCertificateTestMixin:
    def test_create_tls_certificate(self):
        self.gmp.create_tls_certificate("foo", "c1", comment="bar", trust=True)

        self.connection.send.has_been_called_with(
            b"<create_tls_certificate>"
            b"<name>foo</name>"
            b"<certificate>c1</certificate>"
            b"<comment>bar</comment>"
            b"<trust>1</trust>"
            b"</create_tls_certificate>"
        )

        self.gmp.create_tls_certificate("foo", "c1", trust=False)

        self.connection.send.has_been_called_with(
            b"<create_tls_certificate>"
            b"<name>foo</name>"
            b"<certificate>c1</certificate>"
            b"<trust>0</trust>"
            b"</create_tls_certificate>"
        )

    def test_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="foo", certificate="")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="foo", certificate=None)

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name=None, certificate="c1")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="", certificate="c1")
