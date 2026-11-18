# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.next import ActiveDirectoryObjectType


class GetActiveDirectoryObjectTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ActiveDirectoryObjectType.from_string("invalid")

    def test_none_or_empty(self):
        self.assertIsNone(ActiveDirectoryObjectType.from_string(None))
        self.assertIsNone(ActiveDirectoryObjectType.from_string(""))

    def test_ou(self):
        self.assertEqual(
            ActiveDirectoryObjectType.from_string("ou"),
            ActiveDirectoryObjectType.OU,
        )
        self.assertEqual(ActiveDirectoryObjectType.OU.value, "ou")

    def test_container(self):
        self.assertEqual(
            ActiveDirectoryObjectType.from_string("container"),
            ActiveDirectoryObjectType.CONTAINER,
        )
        self.assertEqual(ActiveDirectoryObjectType.CONTAINER.value, "container")

    def test_computer(self):
        self.assertEqual(
            ActiveDirectoryObjectType.from_string("computer"),
            ActiveDirectoryObjectType.COMPUTER,
        )
        self.assertEqual(ActiveDirectoryObjectType.COMPUTER.value, "computer")

    def test_group(self):
        self.assertEqual(
            ActiveDirectoryObjectType.from_string("group"),
            ActiveDirectoryObjectType.GROUP,
        )
        self.assertEqual(ActiveDirectoryObjectType.GROUP.value, "group")
