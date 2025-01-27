# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import CredentialType


class GetCredentialTypeFromStringTestCase(unittest.TestCase):
    def test_invalid_type(self):
        with self.assertRaises(InvalidArgument):
            CredentialType.from_string("foo")

    def test_none_or_empty_type(self):
        ct = CredentialType.from_string(None)
        self.assertIsNone(ct)
        ct = CredentialType.from_string("")
        self.assertIsNone(ct)

    def test_client_certificate(self):
        ct = CredentialType.from_string("client_certificate")
        self.assertEqual(ct, CredentialType.CLIENT_CERTIFICATE)

    def test_snmp(self):
        ct = CredentialType.from_string("snmp")
        self.assertEqual(ct, CredentialType.SNMP)

    def test_username_password(self):
        ct = CredentialType.from_string("username_password")
        self.assertEqual(ct, CredentialType.USERNAME_PASSWORD)

    def test_username_ssh_key(self):
        ct = CredentialType.from_string("username_ssh_key")
        self.assertEqual(ct, CredentialType.USERNAME_SSH_KEY)

    def test_smime_certificate(self):
        ct = CredentialType.from_string("smime_certificate")
        self.assertEqual(ct, CredentialType.SMIME_CERTIFICATE)

    def test_pgp_encryption_key(self):
        ct = CredentialType.from_string("pgp_encryption_key")
        self.assertEqual(ct, CredentialType.PGP_ENCRYPTION_KEY)

    def test_password_only(self):
        ct = CredentialType.from_string("password_only")
        self.assertEqual(ct, CredentialType.PASSWORD_ONLY)
