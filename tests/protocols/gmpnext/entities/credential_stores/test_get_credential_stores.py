# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetCredentialStoresTestMixin:
    def test_get_credential_stores(self):
        self.gmp.get_credential_stores()

        self.connection.send.has_been_called_with(b"<get_credential_stores/>")

    def test_get_credential_stores_with_filter_string(self):
        self.gmp.get_credential_stores(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_credential_stores filter="foo=bar"/>'
        )

    def test_get_credential_stores_with_filter_id(self):
        self.gmp.get_credential_stores(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_credential_stores filt_id="f1"/>'
        )

    def test_get_credential_stores_with_details(self):
        self.gmp.get_credential_stores(details=True)

        self.connection.send.has_been_called_with(
            b'<get_credential_stores details="1"/>'
        )

        self.gmp.get_credential_stores(details=False)

        self.connection.send.has_been_called_with(
            b'<get_credential_stores details="0"/>'
        )

    def test_get_credential_stores_with_id(self):
        self.gmp.get_credential_stores(credential_store_id="cs1")

        self.connection.send.has_been_called_with(
            b"<get_credential_stores>"
            b"<credential_store_id>cs1</credential_store_id>"
            b"</get_credential_stores>"
        )
