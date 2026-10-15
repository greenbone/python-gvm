# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpCreateActiveDirectoryCredentialTestMixin:
    def test_create_ad_credential(self):
        self.gmp.create_active_directory_credential(
            name="AD",
            host="dc.example.org",
            bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
            base_dn="DC=example,DC=org",
            bind_password="secret",
            tls_mode="ldaps",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>AD</name>"
            b"<type>ad</type>"
            b"<host>dc.example.org</host>"
            b"<bind_dn>CN=Scanner,CN=Users,DC=example,DC=org</bind_dn>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<bind_password>secret</bind_password>"
            b"<tls_mode>ldaps</tls_mode>"
            b"</create_credential>"
        )

    def test_create_ad_credential_with_starttls(self):
        self.gmp.create_active_directory_credential(
            name="AD",
            host="dc.example.org",
            bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
            base_dn="DC=example,DC=org",
            bind_password="secret",
            tls_mode="starttls",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>AD</name>"
            b"<type>ad</type>"
            b"<host>dc.example.org</host>"
            b"<bind_dn>CN=Scanner,CN=Users,DC=example,DC=org</bind_dn>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<bind_password>secret</bind_password>"
            b"<tls_mode>starttls</tls_mode>"
            b"</create_credential>"
        )

    def test_create_ad_credential_with_optional_arguments(self):
        self.gmp.create_active_directory_credential(
            name="AD",
            host="dc.example.org",
            bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
            base_dn="DC=example,DC=org",
            bind_password="secret<&",
            tls_mode="ldaps",
            comment="Directory",
            port=636,
            ca_certificate="PEM certificate",
        )

        self.connection.send.has_been_called_with(
            b"<create_credential>"
            b"<name>AD</name>"
            b"<type>ad</type>"
            b"<comment>Directory</comment>"
            b"<host>dc.example.org</host>"
            b"<bind_dn>CN=Scanner,CN=Users,DC=example,DC=org</bind_dn>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<bind_password>secret&lt;&amp;</bind_password>"
            b"<tls_mode>ldaps</tls_mode>"
            b"<port>636</port>"
            b"<ca_certificate>PEM certificate</ca_certificate>"
            b"</create_credential>"
        )

    def test_create_ad_credential_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name=None,
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
            )

    def test_create_ad_credential_missing_host(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
            )

    def test_create_ad_credential_missing_bind_dn(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
            )

    def test_create_ad_credential_missing_base_dn(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="",
                bind_password="secret",
                tls_mode="ldaps",
            )

    def test_create_ad_credential_missing_bind_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="",
                tls_mode="ldaps",
            )

    def test_create_ad_credential_missing_tls_mode(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="",
            )

    def test_create_ad_credential_invalid_tls_mode(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldap",
            )

    def test_create_ad_credential_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
                port=0,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_active_directory_credential(
                name="AD",
                host="dc.example.org",
                bind_dn="CN=Scanner,CN=Users,DC=example,DC=org",
                base_dn="DC=example,DC=org",
                bind_password="secret",
                tls_mode="ldaps",
                port=65536,
            )
