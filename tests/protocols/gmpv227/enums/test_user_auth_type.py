# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import UserAuthType


class GetUserAuthTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            UserAuthType.from_string("foo")

    def test_none_or_empty(self):
        ct = UserAuthType.from_string(None)
        self.assertIsNone(ct)
        ct = UserAuthType.from_string("")
        self.assertIsNone(ct)

    def test_file(self):
        ct = UserAuthType.from_string("file")
        self.assertEqual(ct, UserAuthType.FILE)

    def test_radius_connect(self):
        ct = UserAuthType.from_string("radius_connect")
        self.assertEqual(ct, UserAuthType.RADIUS_CONNECT)

    def test_ldap_connect(self):
        ct = UserAuthType.from_string("ldap_connect")
        self.assertEqual(ct, UserAuthType.LDAP_CONNECT)


if __name__ == "__main__":
    unittest.main()
