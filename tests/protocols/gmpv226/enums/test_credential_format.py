# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import CredentialFormat


class GetCredentialFormatFromStringTestCase(unittest.TestCase):
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
