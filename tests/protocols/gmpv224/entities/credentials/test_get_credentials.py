# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetCredentialsTestMixin:
    def test_get_credentials(self):
        self.gmp.get_credentials()

        self.connection.send.has_been_called_with(b"<get_credentials/>")

    def test_get_credentials_with_filter_string(self):
        self.gmp.get_credentials(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_credentials filter="foo=bar"/>'
        )

    def test_get_credentials_with_filter_id(self):
        self.gmp.get_credentials(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_credentials filt_id="f1"/>'
        )

    def test_get_credentials_with_scanners(self):
        self.gmp.get_credentials(scanners=True)

        self.connection.send.has_been_called_with(
            b'<get_credentials scanners="1"/>'
        )

        self.gmp.get_credentials(scanners=False)

        self.connection.send.has_been_called_with(
            b'<get_credentials scanners="0"/>'
        )

    def test_get_credentials_with_trash(self):
        self.gmp.get_credentials(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_credentials trash="1"/>'
        )

        self.gmp.get_credentials(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_credentials trash="0"/>'
        )

    def test_get_credentials_with_targets(self):
        self.gmp.get_credentials(targets=True)

        self.connection.send.has_been_called_with(
            b'<get_credentials targets="1"/>'
        )

        self.gmp.get_credentials(targets=False)

        self.connection.send.has_been_called_with(
            b'<get_credentials targets="0"/>'
        )
