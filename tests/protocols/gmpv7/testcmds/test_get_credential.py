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

from gvm.errors import InvalidArgumentType, RequiredArgument

from gvm.protocols.gmpv7 import CredentialFormat


class GmpGetCredentialTestCase:
    def test_get_credential(self):
        self.gmp.get_credential('id')

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id"/>'
        )

    def test_get_credentials_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(None)

    def test_get_credentials_invalid_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(credential_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential('')

    def test_get_credential_with_credential_format(self):
        self.gmp.get_credential('id', credential_format=CredentialFormat.KEY)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="key"/>'
        )

        self.gmp.get_credential('id', credential_format=CredentialFormat.RPM)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="rpm"/>'
        )

        self.gmp.get_credential('id', credential_format=CredentialFormat.DEB)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="deb"/>'
        )

        self.gmp.get_credential('id', credential_format=CredentialFormat.EXE)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="exe"/>'
        )

        self.gmp.get_credential('id', credential_format=CredentialFormat.PEM)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="pem"/>'
        )

    def test_get_credential_with_invalid_credential_format(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_credential('id', credential_format='foo')


if __name__ == '__main__':
    unittest.main()
