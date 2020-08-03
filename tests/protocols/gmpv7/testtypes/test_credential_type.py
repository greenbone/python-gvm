# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv7 import CredentialType, get_credential_type_from_string


class GetCredentialTypeFromStringTestCase(unittest.TestCase):
    def test_invalid_type(self):
        with self.assertRaises(InvalidArgument):
            get_credential_type_from_string('foo')

    def test_none_or_empty_type(self):
        ct = get_credential_type_from_string(None)
        self.assertIsNone(ct)
        ct = get_credential_type_from_string('')
        self.assertIsNone(ct)

    def test_client_certificate(self):
        ct = get_credential_type_from_string('client_certificate')
        self.assertEqual(ct, CredentialType.CLIENT_CERTIFICATE)

    def test_snmp(self):
        ct = get_credential_type_from_string('snmp')
        self.assertEqual(ct, CredentialType.SNMP)

    def test_username_password(self):
        ct = get_credential_type_from_string('username_password')
        self.assertEqual(ct, CredentialType.USERNAME_PASSWORD)

    def test_username_ssh_key(self):
        ct = get_credential_type_from_string('username_ssh_key')
        self.assertEqual(ct, CredentialType.USERNAME_SSH_KEY)


if __name__ == '__main__':
    unittest.main()
