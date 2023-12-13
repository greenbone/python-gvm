# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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
from gvm.protocols.gmpv225 import CredentialFormat


class GetCredentialFromatFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            CredentialFormat.from_string("foo")

    def test_none_or_empty(self):
        ct = CredentialFormat.from_string(None)
        self.assertIsNone(ct)
        ct = CredentialFormat.from_string("")
        self.assertIsNone(ct)

    def test_key(self):
        ct = CredentialFormat.from_string("key")
        self.assertEqual(ct, CredentialFormat.KEY)

    def test_rpm(self):
        ct = CredentialFormat.from_string("rpm")
        self.assertEqual(ct, CredentialFormat.RPM)

    def test_deb(self):
        ct = CredentialFormat.from_string("deb")
        self.assertEqual(ct, CredentialFormat.DEB)

    def test_exe(self):
        ct = CredentialFormat.from_string("exe")
        self.assertEqual(ct, CredentialFormat.EXE)

    def test_pem(self):
        ct = CredentialFormat.from_string("pem")
        self.assertEqual(ct, CredentialFormat.PEM)


if __name__ == "__main__":
    unittest.main()
