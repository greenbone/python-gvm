# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from gvm.errors import RequiredArgument, InvalidArgumentType
from gvm.protocols.gmpv9 import (
    CredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)


class GmpCreateCredentialTestCase:
    def test_create_up_credential_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='',
                credential_type=CredentialType.USERNAME_PASSWORD,
                login='foo',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name=None,
                credential_type=CredentialType.USERNAME_PASSWORD,
                login='foo',
            )

    def test_create_up_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment='bar',
            login='Max',
            password='123',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>up</type>'
            '<comment>bar</comment>'
            '<login>Max</login>'
            '<password>123</password>'
            '</create_credential>'
        )

    def test_create_up_credential_with_allow_insecure(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment='bar',
            login='Max',
            password='123',
            allow_insecure=True,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>up</type>'
            '<comment>bar</comment>'
            '<allow_insecure>1</allow_insecure>'
            '<login>Max</login>'
            '<password>123</password>'
            '</create_credential>'
        )

        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.USERNAME_PASSWORD,
            comment='bar',
            login='Max',
            password='123',
            allow_insecure=False,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>up</type>'
            '<comment>bar</comment>'
            '<allow_insecure>0</allow_insecure>'
            '<login>Max</login>'
            '<password>123</password>'
            '</create_credential>'
        )

    def test_create_cc_credential_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo', credential_type=CredentialType.CLIENT_CERTIFICATE
            )

    def test_create_cc_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.CLIENT_CERTIFICATE,
            certificate='abcdef',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>cc</type>'
            '<certificate>abcdef</certificate>'
            '</create_credential>'
        )

    def test_create_cc_credential_with_private_key(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.CLIENT_CERTIFICATE,
            certificate='abcdef',
            private_key='123456',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>cc</type>'
            '<certificate>abcdef</certificate>'
            '<key>'
            '<private>123456</private>'
            '</key>'
            '</create_credential>'
        )

    def test_create_usk_credential_missing_private_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.USERNAME_SSH_KEY,
                login='foo',
            )

    def test_create_usk_credential_missing_login(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.USERNAME_SSH_KEY,
                private_key='123456',
            )

    def test_create_usk_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.USERNAME_SSH_KEY,
            private_key='123456',
            login='foo',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>usk</type>'
            '<login>foo</login>'
            '<key>'
            '<private>123456</private>'
            '</key>'
            '</create_credential>'
        )

    def test_create_usk_credential_with_key_phrase(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.USERNAME_SSH_KEY,
            private_key='123456',
            login='foo',
            key_phrase='abcdef',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>usk</type>'
            '<login>foo</login>'
            '<key>'
            '<private>123456</private>'
            '<phrase>abcdef</phrase>'
            '</key>'
            '</create_credential>'
        )

    def test_create_snmp_credential_invalid_auth_algorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(
                name='foo', credential_type=CredentialType.SNMP, login='foo'
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.SNMP,
                login='foo',
                auth_algorithm='',
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.SNMP,
                login='foo',
                auth_algorithm='bar',
            )

    def test_create_snmp_credential_auth_algorithm_md5(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.MD5,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>md5</auth_algorithm>'
            '</create_credential>'
        )

    def test_create_snmp_credential_auth_algorithm_sha1(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>sha1</auth_algorithm>'
            '</create_credential>'
        )

    def test_create_snmp_credential_with_community(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            community='ipsum',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>sha1</auth_algorithm>'
            '<community>ipsum</community>'
            '</create_credential>'
        )

    def test_create_snmp_credential_invalid_privacy_algorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.SNMP,
                login='foo',
                auth_algorithm=SnmpAuthAlgorithm.SHA1,
                privacy_algorithm='',
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(
                name='foo',
                credential_type=CredentialType.SNMP,
                login='foo',
                auth_algorithm=SnmpAuthAlgorithm.SHA1,
                privacy_algorithm='foo',
            )

    def test_create_snmp_credential_with_privacy_algorithm_aes(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_algorithm=SnmpPrivacyAlgorithm.AES,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>sha1</auth_algorithm>'
            '<privacy>'
            '<algorithm>aes</algorithm>'
            '</privacy>'
            '</create_credential>'
        )

    def test_create_snmp_credential_with_privacy_algorithm_des(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_algorithm=SnmpPrivacyAlgorithm.DES,
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>sha1</auth_algorithm>'
            '<privacy>'
            '<algorithm>des</algorithm>'
            '</privacy>'
            '</create_credential>'
        )

    def test_create_snmp_credential_with_privacy_password(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SNMP,
            login='foo',
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            privacy_password='123',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>snmp</type>'
            '<login>foo</login>'
            '<auth_algorithm>sha1</auth_algorithm>'
            '<privacy>'
            '<password>123</password>'
            '</privacy>'
            '</create_credential>'
        )

    def test_create_smime_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.SMIME_CERTIFICATE,
            certificate='ipsum',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>smime</type>'
            '<certificate>ipsum</certificate>'
            '</create_credential>'
        )

    def test_create_smime_credential_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo', credential_type=CredentialType.SMIME_CERTIFICATE
            )

    def test_create_pgp_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.PGP_ENCRYPTION_KEY,
            public_key='ipsum',
        )

        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>pgp</type>'
            '<key>'
            '<public>ipsum</public>'
            '</key>'
            '</create_credential>'
        )

    def test_create_pgp_credential_missing_public_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo', credential_type=CredentialType.PGP_ENCRYPTION_KEY
            )

    def test_create_credential_invalid_credential_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(name='foo', credential_type=None)

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(name='foo', credential_type='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_credential(name='foo', credential_type='bar')

    def test_create_pw_credential_missing_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_credential(
                name='foo', credential_type=CredentialType.PASSWORD_ONLY
            )

    def test_create_pw_credential(self):
        self.gmp.create_credential(
            name='foo',
            credential_type=CredentialType.PASSWORD_ONLY,
            password='foo',
        )
        self.connection.send.has_been_called_with(
            '<create_credential>'
            '<name>foo</name>'
            '<type>pw</type>'
            '<password>foo</password>'
            '</create_credential>'
        )


if __name__ == '__main__':
    unittest.main()
