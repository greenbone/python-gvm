# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.next import ActiveDirectoryTlsMode


class GetActiveDirectoryTlsModeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ActiveDirectoryTlsMode.from_string("ldap")

    def test_none_or_empty(self):
        self.assertIsNone(ActiveDirectoryTlsMode.from_string(None))
        self.assertIsNone(ActiveDirectoryTlsMode.from_string(""))

    def test_ldaps(self):
        self.assertEqual(
            ActiveDirectoryTlsMode.from_string("ldaps"),
            ActiveDirectoryTlsMode.LDAPS,
        )
        self.assertEqual(ActiveDirectoryTlsMode.LDAPS.value, "ldaps")

    def test_starttls(self):
        self.assertEqual(
            ActiveDirectoryTlsMode.from_string("starttls"),
            ActiveDirectoryTlsMode.STARTTLS,
        )
        self.assertEqual(ActiveDirectoryTlsMode.STARTTLS.value, "starttls")
