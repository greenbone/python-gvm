# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpVerifyActiveDirectoryCredentialTestMixin:
    def test_verify_saved_ad_credential(self):
        self.gmp.verify_active_directory_credential(
            credential_id="credential-id"
        )

        self.connection.send.has_been_called_with(
            b'<verify_active_directory_credential credential_id="credential-id"/>'
        )

    def test_verify_inline_ad_credential(self):
        self.gmp.verify_active_directory_credential(
            host="dc.example.org",
            bind_dn="CN=Scanner,DC=example,DC=org",
            bind_password="secret",
            base_dn="DC=example,DC=org",
            tls_mode="ldaps",
        )

        self.connection.send.has_been_called_with(
            b"<verify_active_directory_credential>"
            b"<host>dc.example.org</host>"
            b"<bind_dn>CN=Scanner,DC=example,DC=org</bind_dn>"
            b"<bind_password>secret</bind_password>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<tls_mode>ldaps</tls_mode>"
            b"</verify_active_directory_credential>"
        )

    def test_verify_inline_ad_credential_with_optional_fields(self):
        self.gmp.verify_active_directory_credential(
            host="dc.example.org",
            bind_dn="CN=Scanner,DC=example,DC=org",
            bind_password="secret<&",
            base_dn="DC=example,DC=org",
            tls_mode="starttls",
            port=389,
            ca_certificate="certificate<&",
        )

        self.connection.send.has_been_called_with(
            b"<verify_active_directory_credential>"
            b"<host>dc.example.org</host>"
            b"<port>389</port>"
            b"<bind_dn>CN=Scanner,DC=example,DC=org</bind_dn>"
            b"<bind_password>secret&lt;&amp;</bind_password>"
            b"<base_dn>DC=example,DC=org</base_dn>"
            b"<tls_mode>starttls</tls_mode>"
            b"<ca_certificate>certificate&lt;&amp;</ca_certificate>"
            b"</verify_active_directory_credential>"
        )

    def test_verify_without_saved_id_or_inline_fields(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.verify_active_directory_credential()

        with self.assertRaises(RequiredArgument):
            self.gmp.verify_active_directory_credential(credential_id="")

    def test_verify_saved_id_with_inline_fields(self):
        for field in ("host", "port", "ca_certificate"):
            with self.subTest(field=field):
                with self.assertRaises(InvalidArgument):
                    self.gmp.verify_active_directory_credential(
                        credential_id="credential-id", **{field: "value"}
                    )

    def test_verify_inline_ad_credential_missing_required_field(self):
        fields = {
            "host": "dc.example.org",
            "bind_dn": "CN=Scanner,DC=example,DC=org",
            "bind_password": "secret",
            "base_dn": "DC=example,DC=org",
            "tls_mode": "ldaps",
        }
        for field in fields:
            with self.subTest(field=field):
                with self.assertRaises(RequiredArgument):
                    self.gmp.verify_active_directory_credential(
                        **{**fields, field: ""}
                    )

    def test_verify_inline_ad_credential_invalid_tls_mode(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.verify_active_directory_credential(
                host="dc.example.org",
                bind_dn="CN=Scanner,DC=example,DC=org",
                bind_password="secret",
                base_dn="DC=example,DC=org",
                tls_mode="ldap",
            )

    def test_verify_inline_ad_credential_invalid_port(self):
        for port in (0, 65536, "389"):
            with self.subTest(port=port):
                with self.assertRaises(InvalidArgument):
                    self.gmp.verify_active_directory_credential(
                        host="dc.example.org",
                        bind_dn="CN=Scanner,DC=example,DC=org",
                        bind_password="secret",
                        base_dn="DC=example,DC=org",
                        tls_mode="ldaps",
                        port=port,
                    )
