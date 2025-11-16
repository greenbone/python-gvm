# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyCredentialStoreCredentialTestMixin:
    def test_modify_cs_credential(self):
        self.gmp.modify_credential_store_credential(credential_id="c1")

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1"/>'
        )

    def test_modify_cs_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential_store_credential(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential_store_credential("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential_store_credential(credential_id="")

    def test_modify_cs_credential_with_name(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", name="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<name>foo</name>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_comment(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", comment="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<comment>foo</comment>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_allow_insecure(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", allow_insecure=True
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<allow_insecure>1</allow_insecure>"
            b"</modify_credential>"
        )

        self.gmp.modify_credential_store_credential(
            credential_id="c1", allow_insecure=False
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<allow_insecure>0</allow_insecure>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_credential_store_id(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", credential_store_id="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<credential_store_id>foo</credential_store_id>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_vault_id(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", vault_id="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<vault_id>foo</vault_id>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_host_identifier(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1", host_identifier="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<host_identifier>foo</host_identifier>"
            b"</modify_credential>"
        )

    def test_modify_cs_credential_with_all(self):
        self.gmp.modify_credential_store_credential(
            credential_id="c1",
            name="foo_name",
            comment="foo_comment",
            credential_store_id="foo_csid",
            vault_id="foo_vid",
            host_identifier="foo_hid",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential credential_id="c1">'
            b"<comment>foo_comment</comment>"
            b"<name>foo_name</name>"
            b"<credential_store_id>foo_csid</credential_store_id>"
            b"<vault_id>foo_vid</vault_id>"
            b"<host_identifier>foo_hid</host_identifier>"
            b"</modify_credential>"
        )
