# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208 import SnmpAuthAlgorithm, SnmpPrivacyAlgorithm


class GmpModifyCredentialTestMixin:
    def test_modify_credential(self):
        self.gmp.modify_credential(credential_id="c1")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1"/>'
        )

    def test_modify_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id="")

    def test_modify_credential_with_name(self):
        self.gmp.modify_credential(credential_id="c1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<name>foo</name>"
            "</modify_credential>"
        )

    def test_modify_credential_with_comment(self):
        self.gmp.modify_credential(credential_id="c1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<comment>foo</comment>"
            "</modify_credential>"
        )

    def test_modify_credential_with_certificate(self):
        self.gmp.modify_credential(credential_id="c1", certificate="abcdef")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<certificate>abcdef</certificate>"
            "</modify_credential>"
        )

    def test_modify_credential_with_private_key_and_key_phrase(self):
        self.gmp.modify_credential(
            credential_id="c1", private_key="123456", key_phrase="foo"
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<key>"
            "<phrase>foo</phrase>"
            "<private>123456</private>"
            "</key>"
            "</modify_credential>"
        )

    def test_modify_credential_missing_private_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id="c1", key_phrase="foo")

    def test_modify_credential_missing_key_phrase(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id="c1", private_key="123456")

    def test_modify_credential_with_allow_insecure(self):
        self.gmp.modify_credential(credential_id="c1", allow_insecure=True)

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<allow_insecure>1</allow_insecure>"
            "</modify_credential>"
        )

        self.gmp.modify_credential(credential_id="c1", allow_insecure=False)

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<allow_insecure>0</allow_insecure>"
            "</modify_credential>"
        )

    def test_modify_credential_with_login(self):
        self.gmp.modify_credential(credential_id="c1", login="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<login>foo</login>"
            "</modify_credential>"
        )

    def test_modify_credential_with_password(self):
        self.gmp.modify_credential(credential_id="c1", password="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<password>foo</password>"
            "</modify_credential>"
        )

    def test_modify_credential_with_auth_algorithm(self):
        self.gmp.modify_credential(
            credential_id="c1", auth_algorithm=SnmpAuthAlgorithm.MD5
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<auth_algorithm>md5</auth_algorithm>"
            "</modify_credential>"
        )

        self.gmp.modify_credential(
            credential_id="c1", auth_algorithm=SnmpAuthAlgorithm.SHA1
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<auth_algorithm>sha1</auth_algorithm>"
            "</modify_credential>"
        )

    def test_modify_credential_invalid_auth_algorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(credential_id="c1", auth_algorithm="foo")

    def test_modify_credential_with_community(self):
        self.gmp.modify_credential(credential_id="c1", community="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<community>foo</community>"
            "</modify_credential>"
        )

    def test_modify_credential_with_privacy_algorithm(self):
        self.gmp.modify_credential(
            credential_id="c1", privacy_algorithm=SnmpPrivacyAlgorithm.AES
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<privacy>"
            "<algorithm>aes</algorithm>"
            "</privacy>"
            "</modify_credential>"
        )

        self.gmp.modify_credential(
            credential_id="c1", privacy_algorithm=SnmpPrivacyAlgorithm.DES
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<privacy>"
            "<algorithm>des</algorithm>"
            "</privacy>"
            "</modify_credential>"
        )

    def test_modify_credential_invalid_privacy_algorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(credential_id="c1", privacy_algorithm="")

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(
                credential_id="c1", privacy_algorithm="foo"
            )

    def test_modify_credential_with_privacy_password(self):
        self.gmp.modify_credential(credential_id="c1", privacy_password="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<privacy>"
            "<password>foo</password>"
            "</privacy>"
            "</modify_credential>"
        )

    def test_modify_credential_with_public_key(self):
        self.gmp.modify_credential(credential_id="c1", public_key="foo")

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            "<key>"
            "<public>foo</public>"
            "</key>"
            "</modify_credential>"
        )
