# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    CredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)


class GmpCreateCredentialTestMixin:
    def test_create_up_credential_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="",
                credential_type=CredentialType.USERNAME_PASSWORD,
                login="foo",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name=None,
                credential_type=CredentialType.USERNAME_PASSWORD,
                login="foo",
            )

    def test_create_up_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment="bar",
            login="Max",
            password="123",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>up</type>"
            b"<comment>bar</comment>"
            b"<login>Max</login>"
            b"<password>123</password>"
            b"</create_credential>"
        )

    def test_create_up_credential_with_allow_insecure(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment="bar",
            login="Max",
            password="123",
            allow_insecure=True,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>up</type>"
            b"<comment>bar</comment>"
            b"<allow_insecure>1</allow_insecure>"
            b"<login>Max</login>"
            b"<password>123</password>"
            b"</create_credential>"
        )

        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment="bar",
            login="Max",
            password="123",
            allow_insecure=False,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>up</type>"
            b"<comment>bar</comment>"
            b"<allow_insecure>0</allow_insecure>"
            b"<login>Max</login>"
            b"<password>123</password>"
            b"</create_credential>"
        )

    def test_create_up_credential_auto_generate_password(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_PASSWORD,
            login="Max",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>up</type>"
            b"<login>Max</login>"
            b"</create_credential>"
        )

    def test_create_cc_credential_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo", credential_type=CredentialType.CLIENT_CERTIFICATE
            )

    def test_create_cc_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.CLIENT_CERTIFICATE,
            certificate="abcdef",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cc</type>"
            b"<certificate>abcdef</certificate>"
            b"</create_credential>"
        )

    def test_create_cc_credential_with_private_key(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.CLIENT_CERTIFICATE,
            certificate="abcdef",
            private_key="123456",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>cc</type>"
            b"<certificate>abcdef</certificate>"
            b"<key>"
            b"<private>123456</private>"
            b"</key>"
            b"</create_credential>"
        )

    def test_create_usk_credential_missing_private_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.USERNAME_SSH_KEY,
                login="foo",
                private_key="",
            )

    def test_create_usk_credential_missing_login(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.USERNAME_SSH_KEY,
                private_key="123456",
            )

    def test_create_usk_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_SSH_KEY,
            private_key="123456",
            login="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>usk</type>"
            b"<login>foo</login>"
            b"<key>"
            b"<private>123456</private>"
            b"</key>"
            b"</create_credential>"
        )

    def test_create_usk_credential_with_key_phrase(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_SSH_KEY,
            private_key="123456",
            login="foo",
            key_phrase="abcdef",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>usk</type>"
            b"<login>foo</login>"
            b"<key>"
            b"<private>123456</private>"
            b"<phrase>abcdef</phrase>"
            b"</key>"
            b"</create_credential>"
        )

    def test_create_usk_credential_auto_generate_ssh_key(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.USERNAME_SSH_KEY,
            login="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>usk</type>"
            b"<login>foo</login>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_invalid_auth_algorithm(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo", credential_type=CredentialType.SNMP, login="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.SNMP,
                login="foo",
                auth_algorithm="",
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.SNMP,
                login="foo",
                auth_algorithm="bar",
            )

    def test_create_snmp_credential_auth_algorithm_md5(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.MD5,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_auth_algorithm_sha1(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_with_community(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            community="ipsum",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"<community>ipsum</community>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_invalid_privacy_algorithm(self):
        with self.assertRaises(ValueError):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.SNMP,
                login="foo",
                auth_algorithm=SnmpAuthAlgorithm.SHA1,
                privacy_algorithm="",
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_credential(
                name="foo",
                credential_type=CredentialType.SNMP,
                login="foo",
                auth_algorithm=SnmpAuthAlgorithm.SHA1,
                privacy_algorithm="foo",
            )

    def test_create_snmp_credential_with_privacy_algorithm_aes(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_algorithm=SnmpPrivacyAlgorithm.AES,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"<privacy>"
            b"<algorithm>aes</algorithm>"
            b"</privacy>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_with_privacy_algorithm_des(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_algorithm=SnmpPrivacyAlgorithm.DES,
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"<privacy>"
            b"<algorithm>des</algorithm>"
            b"</privacy>"
            b"</create_credential>"
        )

    def test_create_snmp_credential_with_privacy_password(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SNMP,
            login="foo",
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_password="123",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>snmp</type>"
            b"<login>foo</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"<privacy>"
            b"<password>123</password>"
            b"</privacy>"
            b"</create_credential>"
        )

    def test_create_smime_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.SMIME_CERTIFICATE,
            certificate="ipsum",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>smime</type>"
            b"<certificate>ipsum</certificate>"
            b"</create_credential>"
        )

    def test_create_smime_credential_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo", credential_type=CredentialType.SMIME_CERTIFICATE
            )

    def test_create_pgp_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.PGP_ENCRYPTION_KEY,
            public_key="ipsum",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>pgp</type>"
            b"<key>"
            b"<public>ipsum</public>"
            b"</key>"
            b"</create_credential>"
        )

    def test_create_pgp_credential_missing_public_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo", credential_type=CredentialType.PGP_ENCRYPTION_KEY
            )

    def test_create_credential_invalid_credential_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(name="foo", credential_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(name="foo", credential_type="")

        with self.assertRaises(InvalidArgument):
            self.gmp.create_credential(name="foo", credential_type="bar")

    def test_create_pw_credential_missing_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name="foo", credential_type=CredentialType.PASSWORD_ONLY
            )

    def test_create_pw_credential(self):
        self.gmp.create_credential(
            name="foo",
            credential_type=CredentialType.PASSWORD_ONLY,
            password="foo",
        )
        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>foo</name>"
            b"<type>pw</type>"
            b"<password>foo</password>"
            b"</create_credential>"
        )
