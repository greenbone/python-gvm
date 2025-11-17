# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyCredentialStoreTestMixin:
    def test_modify_credential_store(self):
        self.gmp.modify_credential_store(credential_store_id="cs1")

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential_store(credential_store_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential_store(credential_store_id="")

    def test_modify_credential_store_with_active(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            active=True,
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<active>1</active>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            active=False,
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<active>0</active>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_host(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            host="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<host>foo</host>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_port(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            port=1234,
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<port>1234</port>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_path(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            path="/foo/bar",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<path>/foo/bar</path>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_comment(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            comment="ahoi",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<comment>ahoi</comment>"
            b"<preferences/>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_app_id(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            app_id="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<app_id>foo</app_id>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_client_cert(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            client_cert="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<client_cert>Zm9v</client_cert>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_client_key(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            client_key="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<client_key>Zm9v</client_key>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_client_pkcs12_file(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            client_pkcs12_file="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<client_pkcs12_file>Zm9v</client_pkcs12_file>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_passphrase(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            passphrase="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<passphrase>foo</passphrase>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_server_ca_cert(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            server_ca_cert="foo",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<preferences>"
            b"<server_ca_cert>Zm9v</server_ca_cert>"
            b"</preferences>"
            b"</modify_credential_store>"
        )

    def test_modify_credential_store_with_all(self):
        self.gmp.modify_credential_store(
            credential_store_id="cs1",
            active=False,
            host="localhost",
            port="80",
            path="/api",
            comment="why was 6 afraid of 7? because 7 8 9",
            app_id="appId",
            client_cert="clientCert",
            client_key="clientKey",
            client_pkcs12_file="clientPkcs12File",
            passphrase="secret",
            server_ca_cert="serverCaCert",
        )

        self.connection.send.has_been_called_with(
            b'<modify_credential_store credential_store_id="cs1">'
            b"<active>0</active>"
            b"<host>localhost</host>"
            b"<port>80</port>"
            b"<path>/api</path>"
            b"<comment>why was 6 afraid of 7? because 7 8 9</comment>"
            b"<preferences>"
            b"<app_id>appId</app_id>"
            b"<client_cert>Y2xpZW50Q2VydA==</client_cert>"
            b"<client_key>Y2xpZW50S2V5</client_key>"
            b"<client_pkcs12_file>Y2xpZW50UGtjczEyRmlsZQ==</client_pkcs12_file>"
            b"<passphrase>secret</passphrase>"
            b"<server_ca_cert>c2VydmVyQ2FDZXJ0</server_ca_cert>"
            b"</preferences>"
            b"</modify_credential_store>"
        )
