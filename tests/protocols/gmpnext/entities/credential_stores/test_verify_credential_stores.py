# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpVerifyCredentialStoreTestMixin:
    def test_verify_credential_store(self):
        self.gmp.verify_credential_store(credential_store_id="cs1")

        self.connection.send.has_been_called_with(
            b'<verify_credential_store credential_store_id="cs1"/>'
        )

    def test_verify_credential_store_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.verify_credential_store(credential_store_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.verify_credential_store(credential_store_id="")
