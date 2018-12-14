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

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection

class GmpGetCredentialTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_get_credential_simple(self):
        self.gmp.get_credential('id')

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id"/>')

    def test_fail_without_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential(None)

    def test_fail_with_empty_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_credential('')

    def test_get_credential_with_valid_format(self):
        self.gmp.get_credential('id', credential_format='key')

        self.connection.send.has_been_called_with(
            '<get_credentials credential_id="id" format="key"/>')

    def test_get_credential_with_invalid_format(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_credential('id', credential_format='foo')


if __name__ == '__main__':
    unittest.main()
