# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateTLSCertificateTestMixin:
    def test_create_tls_certificate(self):
        self.gmp.create_tls_certificate("foo", "c1", comment="bar", trust=True)

        self.connection.send.has_been_called_with(
            "<create_tls_certificate>"
            "<comment>bar</comment>"
            "<name>foo</name>"
            "<certificate>c1</certificate>"
            "<trust>1</trust>"
            "</create_tls_certificate>"
        )

        self.gmp.create_tls_certificate("foo", "c1", trust=False)

        self.connection.send.has_been_called_with(
            "<create_tls_certificate>"
            "<name>foo</name>"
            "<certificate>c1</certificate>"
            "</create_tls_certificate>"
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
