# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetHostsTestMixin:
    def test_get_hosts(self):
        self.gmp.get_hosts()

        self.connection.send.has_been_called_with(b'<get_assets type="host"/>')

    def test_get_hosts_details(self):
        self.gmp.get_hosts(details=True)

        self.connection.send.has_been_called_with(
            b'<get_assets type="host" details="1"/>'
        )

        self.gmp.get_hosts(details=False)

        self.connection.send.has_been_called_with(
            b'<get_assets type="host" details="0"/>'
        )

    def test_get_hosts_with_filter_string(self):
        self.gmp.get_hosts(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_assets type="host" filter="foo=bar"/>'
        )

    def test_get_hosts_with_filter_id(self):
        self.gmp.get_hosts(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_assets type="host" filt_id="f1"/>'
        )
