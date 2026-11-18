# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.next import ActiveDirectorySearchScope


class GetActiveDirectorySearchScopeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ActiveDirectorySearchScope.from_string("invalid")

    def test_none_or_empty(self):
        self.assertIsNone(ActiveDirectorySearchScope.from_string(None))
        self.assertIsNone(ActiveDirectorySearchScope.from_string(""))

    def test_base(self):
        self.assertEqual(
            ActiveDirectorySearchScope.from_string("base"),
            ActiveDirectorySearchScope.BASE,
        )
        self.assertEqual(ActiveDirectorySearchScope.BASE.value, "base")

    def test_onelevel(self):
        self.assertEqual(
            ActiveDirectorySearchScope.from_string("onelevel"),
            ActiveDirectorySearchScope.ONELEVEL,
        )
        self.assertEqual(ActiveDirectorySearchScope.ONELEVEL.value, "onelevel")

    def test_subtree(self):
        self.assertEqual(
            ActiveDirectorySearchScope.from_string("subtree"),
            ActiveDirectorySearchScope.SUBTREE,
        )
        self.assertEqual(ActiveDirectorySearchScope.SUBTREE.value, "subtree")
