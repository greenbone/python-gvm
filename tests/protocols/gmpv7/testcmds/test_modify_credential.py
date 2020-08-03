# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

from gvm.protocols.gmpv7 import SnmpAuthAlgorithm, SnmpPrivacyAlgorithm


class GmpModifyCredentialTestCase:
    def test_modify_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential('')

    def test_modify_credential_with_comment(self):
        self.gmp.modify_credential(credential_id='c1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<comment>foo</comment>'
            '</modify_credential>'
        )

    def test_modify_credential_with_name(self):
        self.gmp.modify_credential(credential_id='c1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<name>foo</name>'
            '</modify_credential>'
        )

    def test_modify_credential_with_allow_insecure(self):
        self.gmp.modify_credential(credential_id='c1', allow_insecure=True)

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<allow_insecure>1</allow_insecure>'
            '</modify_credential>'
        )

        self.gmp.modify_credential(credential_id='c1', allow_insecure=False)

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<allow_insecure>0</allow_insecure>'
            '</modify_credential>'
        )

    def test_modify_credential_with_certificate(self):
        self.gmp.modify_credential(credential_id='c1', certificate='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<certificate>foo</certificate>'
            '</modify_credential>'
        )

    def test_modify_credential_with_private_key(self):
        self.gmp.modify_credential(credential_id='c1', private_key='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<key>'
            '<private>foo</private>'
            '</key>'
            '</modify_credential>'
        )

    def test_modify_credential_with_key_phrase_and_private_key(self):
        self.gmp.modify_credential(
            credential_id='c1', key_phrase='', private_key='foo'
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<key>'
            '<private>foo</private>'
            '<phrase></phrase>'
            '</key>'
            '</modify_credential>'
        )

        self.gmp.modify_credential(
            credential_id='c1', key_phrase='bar', private_key='foo'
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<key>'
            '<private>foo</private>'
            '<phrase>bar</phrase>'
            '</key>'
            '</modify_credential>'
        )

    def test_modify_credential_with_key_phrase_and_missing_private_key(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(
                credential_id='c1', key_phrase='', private_key=''
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(credential_id='c1', key_phrase='bar')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_credential(
                credential_id='c1', key_phrase='bar', private_key=None
            )

    def test_modify_credential_with_login(self):
        self.gmp.modify_credential(credential_id='c1', login='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<login>foo</login>'
            '</modify_credential>'
        )

    def test_modify_credential_with_password(self):
        self.gmp.modify_credential(credential_id='c1', password='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<password>foo</password>'
            '</modify_credential>'
        )

    def test_modify_credential_with_community(self):
        self.gmp.modify_credential(credential_id='c1', community='foo')

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<community>foo</community>'
            '</modify_credential>'
        )

    def test_modify_credential_with_privacy_alogorithm(self):
        self.gmp.modify_credential(
            credential_id='c1', privacy_algorithm=SnmpPrivacyAlgorithm.AES
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<privacy>'
            '<algorithm>aes</algorithm>'
            '</privacy>'
            '</modify_credential>'
        )

        self.gmp.modify_credential(
            credential_id='c1', privacy_algorithm=SnmpPrivacyAlgorithm.DES
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<privacy>'
            '<algorithm>des</algorithm>'
            '</privacy>'
            '</modify_credential>'
        )

    def test_modify_credential_with_privacy_alogorithm_and_password(self):
        self.gmp.modify_credential(
            credential_id='c1',
            privacy_algorithm=SnmpPrivacyAlgorithm.AES,
            privacy_password='foo',
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<privacy>'
            '<algorithm>aes</algorithm>'
            '<password>foo</password>'
            '</privacy>'
            '</modify_credential>'
        )

        self.gmp.modify_credential(
            credential_id='c1',
            privacy_algorithm=SnmpPrivacyAlgorithm.AES,
            privacy_password='',
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<privacy>'
            '<algorithm>aes</algorithm>'
            '<password></password>'
            '</privacy>'
            '</modify_credential>'
        )

    def test_modify_credential_invalid_privacy_alogorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(credential_id='c1', privacy_algorithm='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(
                credential_id='c1', privacy_algorithm='foo'
            )

    def test_modify_credential_with_auth_alogorithm(self):
        self.gmp.modify_credential(
            credential_id='c1', auth_algorithm=SnmpAuthAlgorithm.MD5
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<auth_algorithm>md5</auth_algorithm>'
            '</modify_credential>'
        )

        self.gmp.modify_credential(
            credential_id='c1', auth_algorithm=SnmpAuthAlgorithm.SHA1
        )

        self.connection.send.has_been_called_with(
            '<modify_credential credential_id="c1">'
            '<auth_algorithm>sha1</auth_algorithm>'
            '</modify_credential>'
        )

    def test_modify_credential_invalid_auth_alogorithm(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(credential_id='c1', auth_algorithm='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_credential(credential_id='c1', auth_algorithm='foo')


if __name__ == '__main__':
    unittest.main()
