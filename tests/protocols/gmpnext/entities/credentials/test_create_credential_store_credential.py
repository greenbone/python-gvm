# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.next import CredentialStoreCredentialType


class GmpCreateCredentialStoreCredentialTestMixin:
    def test_create_cs_up_credential_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name="",
                credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
                vault_id="foo",
                host_identifier="bar",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name=None,
                credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
                vault_id="foo",
                host_identifier="bar",
            )

    def test_create_cs_up_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
            comment="bar",
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_up</type>"
            b"<comment>bar</comment>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_up_credential_with_credential_store_id(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
            comment="bar",
            credential_store_id="abc",
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_up</type>"
            b"<comment>bar</comment>"
            b"<credential_store_id>abc</credential_store_id>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_up_credential_with_missing_vault_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name="foo",
                credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
                comment="bar",
                host_identifier="456",
            )

    def test_create_cs_up_credential_with_missing_host_identifier(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name="foo",
                credential_type=CredentialStoreCredentialType.USERNAME_PASSWORD,
                comment="bar",
                vault_id="123",
            )

    def test_create_cs_cc_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.CLIENT_CERTIFICATE,
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_cc</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_usk_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.USERNAME_SSH_KEY,
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_usk</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_snmp_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.SNMP,
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_snmp</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_smime_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.SMIME_CERTIFICATE,
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_smime</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_pgp_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.PGP_ENCRYPTION_KEY,
            vault_id="123",
            host_identifier="456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_pgp</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )

    def test_create_cs_credential_invalid_credential_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name="foo", credential_type=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential_store_credential(
                name="foo", credential_type=""
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_credential_store_credential(
                name="foo", credential_type="bar"
            )

    def test_create_cs_pw_credential(self):
        self.gmp.create_credential_store_credential(
            name="foo",
            credential_type=CredentialStoreCredentialType.PASSWORD_ONLY,
            vault_id="123",
            host_identifier="456",
        )
        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cs_pw</type>"
            b"<vault_id>123</vault_id>"
            b"<host_identifier>456</host_identifier>"
            b"</create_credential>"
        )
