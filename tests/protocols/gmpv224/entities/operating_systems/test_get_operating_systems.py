# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetOperatingSystemsTestMixin:
    def test_get_operating_systems(self):
        self.gmp.get_operating_systems()

        self.connection.send.has_been_called_with(b'<get_assets type="os"/>')

    def test_get_operating_systems_details(self):
        self.gmp.get_operating_systems(details=True)

        self.connection.send.has_been_called_with(
            b'<get_assets type="os" details="1"/>'
        )

        self.gmp.get_operating_systems(details=False)

        self.connection.send.has_been_called_with(
            b'<get_assets type="os" details="0"/>'
        )

    def test_get_operating_systems_with_filter_string(self):
        self.gmp.get_operating_systems(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_assets type="os" filter="foo=bar"/>'
        )

    def test_get_operating_systems_with_filter_id(self):
        self.gmp.get_operating_systems(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_assets type="os" filt_id="f1"/>'
        )
