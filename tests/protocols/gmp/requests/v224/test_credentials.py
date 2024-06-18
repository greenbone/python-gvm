# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    CredentialFormat,
    Credentials,
    CredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)


class CredentialsTestCase(unittest.TestCase):
    def test_clone_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            Credentials.clone_credential(None)

        with self.assertRaises(RequiredArgument):
            Credentials.clone_credential("")

    def test_clone_credential(self):
        request = Credentials.clone_credential("a1")
        self.assertEqual(
            bytes(request),
            b"<create_credential><copy>a1</copy></create_credential>",
        )

    def test_create_credential_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                None, CredentialType.PASSWORD_ONLY, password="password"
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "", CredentialType.PASSWORD_ONLY, password="password"
            )

    def test_create_credential_missing_credential_type(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential("name", None)

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential("name", "")

    def test_create_credential_invalid_credential_type(self):
        with self.assertRaises(InvalidArgument):
            Credentials.create_credential("name", "invalid")

    def test_create_credential_username_password(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_PASSWORD,
            login="username",
            password="password",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>up</type>"
            b"<login>username</login>"
            b"<password>password</password>"
            b"</create_credential>",
        )

    def test_create_credential_username_password_auto_generate_password(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_PASSWORD,
            login="username",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>up</type>"
            b"<login>username</login>"
            b"</create_credential>",
        )

    def test_create_username_password_credential_with_allow_insecure(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_PASSWORD,
            login="username",
            password="password",
            allow_insecure=True,
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>up</type>"
            b"<allow_insecure>1</allow_insecure>"
            b"<login>username</login>"
            b"<password>password</password>"
            b"</create_credential>",
        )

    def test_create_credential_username_password_with_comment(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_PASSWORD,
            login="username",
            password="password",
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>up</type>"
            b"<comment>comment</comment>"
            b"<login>username</login>"
            b"<password>password</password>"
            b"</create_credential>",
        )

    def test_create_credential_username_password_missing_login(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.USERNAME_PASSWORD, password="password"
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.USERNAME_PASSWORD,
                login="",
                password="password",
            )

    def test_create_credential_client_certificate(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.CLIENT_CERTIFICATE,
            certificate="certificate",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>cc</type>"
            b"<certificate>certificate</certificate>"
            b"</create_credential>",
        )

    def test_create_credential_client_certificate_with_private_key(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.CLIENT_CERTIFICATE,
            certificate="certificate",
            private_key="private_key",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>cc</type>"
            b"<certificate>certificate</certificate>"
            b"<key>"
            b"<private>private_key</private>"
            b"</key>"
            b"</create_credential>",
        )

    def test_create_credential_client_certificate_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.CLIENT_CERTIFICATE
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.CLIENT_CERTIFICATE, certificate=""
            )

    def test_create_credential_username_ssh_key(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_SSH_KEY,
            login="username",
            private_key="private",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>usk</type>"
            b"<login>username</login>"
            b"<key>"
            b"<private>private</private>"
            b"</key>"
            b"</create_credential>",
        )

    def test_create_credential_username_ssh_key_with_passphrase(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_SSH_KEY,
            login="username",
            private_key="private",
            key_phrase="passphrase",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>usk</type>"
            b"<login>username</login>"
            b"<key>"
            b"<private>private</private>"
            b"<phrase>passphrase</phrase>"
            b"</key>"
            b"</create_credential>",
        )

    def test_create_credential_username_ssh_key_auto_generate_key(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.USERNAME_SSH_KEY,
            login="username",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>usk</type>"
            b"<login>username</login>"
            b"</create_credential>",
        )

    def test_create_credential_username_ssh_key_missing_private_key(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.USERNAME_SSH_KEY,
                login="username",
                private_key="",
            )

    def test_create_credential_username_ssh_key_missing_login(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.USERNAME_SSH_KEY, private_key="private"
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.USERNAME_SSH_KEY,
                login="",
                private_key="private",
            )

    def test_create_credential_snmp_with_auth_algorithm_md5(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.MD5,
            login="username",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"</create_credential>",
        )

    def test_create_credential_snmp_with_auth_algorithm_sha1(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            login="username",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"</create_credential>",
        )

    def test_create_credential_snmp_missing_auth_algorithm(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.SNMP, login="username"
            )
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SNMP,
                login="username",
                auth_algorithm=None,
            )
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SNMP,
                login="username",
                auth_algorithm="",
            )

    def test_create_credential_snmp_missing_login(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SNMP,
                auth_algorithm=SnmpAuthAlgorithm.MD5,
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SNMP,
                auth_algorithm=SnmpAuthAlgorithm.MD5,
                login="",
            )

    def test_create_credential_snmp_with_community(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.MD5,
            login="username",
            community="community",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"<community>community</community>"
            b"</create_credential>",
        )

    def test_create_credential_snmp_with_password(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.MD5,
            login="username",
            password="password",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<password>password</password>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"</create_credential>",
        )

    def test_create_credential_snmp_with_privacy_algorithm(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.MD5,
            login="username",
            privacy_algorithm=SnmpPrivacyAlgorithm.DES,
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"<privacy>"
            b"<algorithm>des</algorithm>"
            b"</privacy>"
            b"</create_credential>",
        )

    def test_create_credential_snmp_with_privacy_algorithm_and_privacy_password(
        self,
    ):
        request = Credentials.create_credential(
            "name",
            CredentialType.SNMP,
            auth_algorithm=SnmpAuthAlgorithm.MD5,
            login="username",
            privacy_algorithm=SnmpPrivacyAlgorithm.DES,
            privacy_password="password",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>snmp</type>"
            b"<login>username</login>"
            b"<auth_algorithm>md5</auth_algorithm>"
            b"<privacy>"
            b"<algorithm>des</algorithm>"
            b"<password>password</password>"
            b"</privacy>"
            b"</create_credential>",
        )

    def test_create_credential_pgp(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.PGP_ENCRYPTION_KEY,
            public_key="public_key",
        )

        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>pgp</type>"
            b"<key>"
            b"<public>public_key</public>"
            b"</key>"
            b"</create_credential>",
        )

    def test_create_credential_pgp_missing_key(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.PGP_ENCRYPTION_KEY
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.PGP_ENCRYPTION_KEY, public_key=None
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.PGP_ENCRYPTION_KEY, public_key=""
            )

    def test_create_credential_password_only(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.PASSWORD_ONLY,
            password="password",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>pw</type>"
            b"<password>password</password>"
            b"</create_credential>",
        )

    def test_create_credential_password_only_missing_password(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential("name", CredentialType.PASSWORD_ONLY)

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.PASSWORD_ONLY, password=None
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name", CredentialType.PASSWORD_ONLY, password=""
            )

    def test_create_credential_smime(self):
        request = Credentials.create_credential(
            "name",
            CredentialType.SMIME_CERTIFICATE,
            certificate="certificate",
        )
        self.assertEqual(
            bytes(request),
            b"<create_credential>"
            b"<name>name</name>"
            b"<type>smime</type>"
            b"<certificate>certificate</certificate>"
            b"</create_credential>",
        )

    def test_create_credential_smime_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SMIME_CERTIFICATE,
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SMIME_CERTIFICATE,
                certificate=None,
            )

        with self.assertRaises(RequiredArgument):
            Credentials.create_credential(
                "name",
                CredentialType.SMIME_CERTIFICATE,
                certificate="",
            )

    def test_delete_alert(self):
        request = Credentials.delete_credential("a1")
        self.assertEqual(
            bytes(request),
            b'<delete_credential credential_id="a1" ultimate="0"/>',
        )

    def test_delete_alert_with_ultimate(self):
        request = Credentials.delete_credential("a1", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_credential credential_id="a1" ultimate="0"/>',
        )

        request = Credentials.delete_credential("a1", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_credential credential_id="a1" ultimate="1"/>',
        )

    def test_delete_alert_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            Credentials.delete_credential(None)

        with self.assertRaises(RequiredArgument):
            Credentials.delete_credential("")

    def test_get_credentials(self):
        request = Credentials.get_credentials()
        self.assertEqual(
            bytes(request),
            b"<get_credentials/>",
        )

    def test_get_credentials_with_filter_string(self):
        request = Credentials.get_credentials(filter_string="name")
        self.assertEqual(
            bytes(request),
            b'<get_credentials filter="name"/>',
        )

    def test_get_credentials_with_scanners(self):
        request = Credentials.get_credentials(scanners=True)
        self.assertEqual(
            bytes(request),
            b'<get_credentials scanners="1"/>',
        )

    def test_get_credentials_with_trash(self):
        request = Credentials.get_credentials(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_credentials trash="1"/>',
        )

    def test_get_credentials_with_targets(self):
        request = Credentials.get_credentials(targets=True)
        self.assertEqual(
            bytes(request),
            b'<get_credentials targets="1"/>',
        )

    def test_get_credential(self):
        request = Credentials.get_credential("a1")
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1"/>',
        )

    def test_get_credential_with_scanners(self):
        request = Credentials.get_credential("a1", scanners=True)
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" scanners="1"/>',
        )

    def test_get_credential_with_targets(self):
        request = Credentials.get_credential("a1", targets=True)
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" targets="1"/>',
        )

    def test_get_credential_with_credential_format(self):
        request = Credentials.get_credential("a1", credential_format="key")
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="key"/>',
        )

        request = Credentials.get_credential(
            "a1", credential_format=CredentialFormat.KEY
        )
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="key"/>',
        )

        request = Credentials.get_credential(
            "a1", credential_format=CredentialFormat.EXE
        )
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="exe"/>',
        )

        request = Credentials.get_credential(
            "a1", credential_format=CredentialFormat.DEB
        )
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="deb"/>',
        )

        request = Credentials.get_credential(
            "a1", credential_format=CredentialFormat.PEM
        )
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="pem"/>',
        )

        request = Credentials.get_credential(
            "a1", credential_format=CredentialFormat.RPM
        )
        self.assertEqual(
            bytes(request),
            b'<get_credentials credential_id="a1" format="rpm"/>',
        )

    def test_get_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            Credentials.get_credential(None)

        with self.assertRaises(RequiredArgument):
            Credentials.get_credential("")

    def test_modify_credential_with_name(self):
        request = Credentials.modify_credential("a1", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<name>name</name>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_comment(self):
        request = Credentials.modify_credential("a1", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<comment>comment</comment>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_allow_insecure(self):
        request = Credentials.modify_credential("a1", allow_insecure=True)
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<allow_insecure>1</allow_insecure>"
            b"</modify_credential>",
        )
        request = Credentials.modify_credential("a1", allow_insecure=False)
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<allow_insecure>0</allow_insecure>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_certificate(self):
        request = Credentials.modify_credential("a1", certificate="certificate")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<certificate>certificate</certificate>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_key_phrase_and_private_key(self):
        request = Credentials.modify_credential(
            "a1", key_phrase="passphrase", private_key="private"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<key>"
            b"<phrase>passphrase</phrase>"
            b"<private>private</private>"
            b"</key>"
            b"</modify_credential>",
        )

    def test_modify_credential_missing_key_phrase_or_private_key(self):
        with self.assertRaises(RequiredArgument):
            Credentials.modify_credential("a1", key_phrase="passphrase")

        with self.assertRaises(RequiredArgument):
            Credentials.modify_credential("a1", private_key="private")

    def test_modify_credential_with_login(self):
        request = Credentials.modify_credential("a1", login="username")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<login>username</login>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_password(self):
        request = Credentials.modify_credential("a1", password="password")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<password>password</password>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_auth_algorithm(self):
        request = Credentials.modify_credential(
            "a1", auth_algorithm=SnmpAuthAlgorithm.MD5
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<auth_algorithm>md5</auth_algorithm>"
            b"</modify_credential>",
        )

        request = Credentials.modify_credential("a1", auth_algorithm="md5")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<auth_algorithm>md5</auth_algorithm>"
            b"</modify_credential>",
        )

        request = Credentials.modify_credential(
            "a1", auth_algorithm=SnmpAuthAlgorithm.SHA1
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<auth_algorithm>sha1</auth_algorithm>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_community(self):
        request = Credentials.modify_credential("a1", community="community")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<community>community</community>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_privacy_algorithm(self):
        request = Credentials.modify_credential(
            "a1", privacy_algorithm=SnmpPrivacyAlgorithm.DES
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<privacy>"
            b"<algorithm>des</algorithm>"
            b"</privacy>"
            b"</modify_credential>",
        )

        request = Credentials.modify_credential("a1", privacy_algorithm="des")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<privacy>"
            b"<algorithm>des</algorithm>"
            b"</privacy>"
            b"</modify_credential>",
        )

        request = Credentials.modify_credential(
            "a1", privacy_algorithm=SnmpPrivacyAlgorithm.AES
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<privacy>"
            b"<algorithm>aes</algorithm>"
            b"</privacy>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_privacy_password(self):
        request = Credentials.modify_credential(
            "a1", privacy_password="password"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<privacy>"
            b"<password>password</password>"
            b"</privacy>"
            b"</modify_credential>",
        )

    def test_modify_credential_with_public_key(self):
        request = Credentials.modify_credential("a1", public_key="public_key")
        self.assertEqual(
            bytes(request),
            b'<modify_credential credential_id="a1">'
            b"<key>"
            b"<public>public_key</public>"
            b"</key>"
            b"</modify_credential>",
        )

    def test_modify_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            Credentials.modify_credential(None)

        with self.assertRaises(RequiredArgument):
            Credentials.modify_credential("")
