# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
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

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208 import CredentialFormat


class GmpGetCredentialTestMixin:
    def test_get_credential(self):
        self.gmp.get_credential("id")

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id"/>'
        )

    def test_get_credential_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(None)

    def test_get_credential_invalid_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(credential_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential("")

    def test_get_credential_with_credential_format(self):
        self.gmp.get_credential("id", credential_format=CredentialFormat.KEY)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="key"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.RPM)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="rpm"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.DEB)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="deb"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.EXE)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="exe"/>'
        )

        self.gmp.get_credential("id", credential_format=CredentialFormat.PEM)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="pem"/>'
        )

    def test_get_credential_with_invalid_credential_format(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_credential("id", credential_format="foo")

    def test_get_credential_with_scanners(self):
        self.gmp.get_credential("id", scanners=True)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" scanners="1"/>'
        )

        self.gmp.get_credential("id", scanners=False)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" scanners="0"/>'
        )

    def test_get_credential_with_targets(self):
        self.gmp.get_credential("id", targets=True)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" targets="1"/>'
        )

        self.gmp.get_credential("id", targets=False)

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" targets="0"/>'
        )
