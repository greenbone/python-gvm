# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import CredentialFormat


class GmpGetCredentialTestMixin:
    def test_get_credential(self):
        self.gmp.get_credential("id")

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id"/>'
        )

    def test_get_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(None)

    def test_get_credential_invalid_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(credential_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential("")

    def test_get_credential_with_credential_format(self):
        self.gmp.get_credential("id", credential_format=CredentialFormat.KEY)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" format="key"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.RPM)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" format="rpm"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.DEB)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" format="deb"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.EXE)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" format="exe"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.PEM)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" format="pem"/>'
        )

    def test_get_credential_with_invalid_credential_format(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_credential("id", credential_format="foo")

    def test_get_credential_with_scanners(self):
        self.gmp.get_credential("id", scanners=True)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" scanners="1"/>'
        )

        self.gmp.get_credential("id", scanners=False)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" scanners="0"/>'
        )

    def test_get_credential_with_targets(self):
        self.gmp.get_credential("id", targets=True)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" targets="1"/>'
        )

        self.gmp.get_credential("id", targets=False)

        self.connection.send.has_been_called_with(
            b'<get_credentials credential_id="id" targets="0"/>'
        )
