# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpModifyActiveDirectoryCredentialTestMixin:
    def test_modify_ad_credential(self):
        self.gmp.modify_active_directory_credential(
            credential_id="credential-id"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="credential-id"/>'
        )

    def test_modify_ad_credential_with_all_arguments(self):
        self.gmp.modify_active_directory_credential(
            credential_id="credential-id",
            name="AD",
            comment="Directory",
            host="dc.example.org",
            bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
            base_dn="DC=example,DC=org",
            bind_password="secret<&",
            tls_mode="ldaps",
            port=636,
            ca_certificate="PEM certificate",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="credential-id">'
            b"<name>AD</name>"
            b"<comment>Directory</comment>"
            b"<host>dc.example.org</host>"
            b"<bind_dn>CN=Scanner,CN=Users,DC=example,DC=org</bind_dn>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<bind_password>secret&lt;&amp;</bind_password>"
            b"<tls_mode>ldaps</tls_mode>"
            b"<port>636</port>"
            b"<ca_certificate>PEM certificate</ca_certificate>"
            b"</modify_credential>"
        )

    def test_modify_ad_credential_with_bind_password(self):
        self.gmp.modify_active_directory_credential(
            credential_id="credential-id", bind_password="new-secret"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="credential-id">'
            b"<bind_password>new-secret</bind_password>"
            b"</modify_credential>"
        )

    def test_modify_ad_credential_clear_optional_arguments(self):
        self.gmp.modify_active_directory_credential(
            credential_id="credential-id",
            comment="",
            port="",
            ca_certificate="",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="credential-id">'
            b"<comment></comment>"
            b"<port></port>"
            b"<ca_certificate></ca_certificate>"
            b"</modify_credential>"
        )

    def test_modify_ad_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(credential_id="")

    def test_modify_ad_credential_empty_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", name=""
            )

    def test_modify_ad_credential_empty_host(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", host=""
            )

    def test_modify_ad_credential_empty_bind_dn(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", bind_dn=""
            )

    def test_modify_ad_credential_empty_base_dn(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", base_dn=""
            )

    def test_modify_ad_credential_empty_bind_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", bind_password=""
            )

    def test_modify_ad_credential_empty_tls_mode(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", tls_mode=""
            )

    def test_modify_ad_credential_invalid_tls_mode(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", tls_mode="ldap"
            )

    def test_modify_ad_credential_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", port=0
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", port=65536
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_active_directory_credential(
                credential_id="credential-id", port="636"
            )
