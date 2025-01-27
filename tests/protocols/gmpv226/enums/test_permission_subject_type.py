# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import PermissionSubjectType


class GetPermissionSubjectTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            PermissionSubjectType.from_string("foo")

    def test_none_or_empty(self):
        ct = PermissionSubjectType.from_string(None)
        self.assertIsNone(ct)
        ct = PermissionSubjectType.from_string("")
        self.assertIsNone(ct)

    def test_user(self):
        ct = PermissionSubjectType.from_string("user")
        self.assertEqual(ct, PermissionSubjectType.USER)

    def test_role(self):
        ct = PermissionSubjectType.from_string("role")
        self.assertEqual(ct, PermissionSubjectType.ROLE)

    def test_group(self):
        ct = PermissionSubjectType.from_string("group")
        self.assertEqual(ct, PermissionSubjectType.GROUP)
