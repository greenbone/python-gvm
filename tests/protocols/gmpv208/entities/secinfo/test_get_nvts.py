# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetNvtListTestMixin:
    def test_get_nvts(self):
        self.gmp.get_nvts()

        self.connection.send.has_been_called_with(b'<get_info type="NVT"/>')

    def test_get_nvts_with_filter_string(self):
        self.gmp.get_nvts(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="NVT" filter="foo=bar"/>'
        )

    def test_get_nvts_with_filter_id(self):
        self.gmp.get_nvts(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="NVT" filt_id="f1"/>'
        )

    def test_get_nvts_with_name(self):
        self.gmp.get_nvts(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="NVT" name="foo"/>'
        )

    def test_get_nvts_with_details(self):
        self.gmp.get_nvts(details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="NVT" details="1"/>'
        )

        self.gmp.get_nvts(details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="NVT" details="0"/>'
        )

    def test_get_extended_nvts(self):
        self.gmp.get_nvts(extended=True)

        self.connection.send.has_been_called_with(b"<get_nvts/>")

    def test_get_extended_nvts_with_details(self):
        self.gmp.get_nvts(extended=True, details=True)

        self.connection.send.has_been_called_with(b'<get_nvts details="1"/>')

        self.gmp.get_nvts(extended=True, details=False)

        self.connection.send.has_been_called_with(b'<get_nvts details="0"/>')

    def test_get_extended_nvts_with_preferences(self):
        self.gmp.get_nvts(extended=True, preferences=True)

        self.connection.send.has_been_called_with(
            b'<get_nvts preferences="1"/>'
        )

        self.gmp.get_nvts(extended=True, preferences=False)

        self.connection.send.has_been_called_with(
            b'<get_nvts preferences="0"/>'
        )

    def test_get_extended_nvts_with_preference_count(self):
        self.gmp.get_nvts(extended=True, preference_count=True)

        self.connection.send.has_been_called_with(
            b'<get_nvts preference_count="1"/>'
        )

    def test_get_extended_nvts_with_timeout(self):
        self.gmp.get_nvts(extended=True, timeout=True)

        self.connection.send.has_been_called_with(b'<get_nvts timeout="1"/>')

        self.gmp.get_nvts(extended=True, timeout=False)

        self.connection.send.has_been_called_with(b'<get_nvts timeout="0"/>')

    def test_get_extended_nvts_with_config_id(self):
        self.gmp.get_nvts(extended=True, config_id="config_id")

        self.connection.send.has_been_called_with(
            b'<get_nvts config_id="config_id"/>'
        )

    def test_get_extended_nvts_with_preferences_config_id(self):
        self.gmp.get_nvts(
            extended=True, preferences_config_id="preferences_config_id"
        )

        self.connection.send.has_been_called_with(
            b'<get_nvts preferences_config_id="preferences_config_id"/>'
        )

    def test_get_extended_nvts_with_family(self):
        self.gmp.get_nvts(extended=True, family="family")

        self.connection.send.has_been_called_with(
            b'<get_nvts family="family"/>'
        )

    def test_get_extended_nvts_with_sort_order(self):
        self.gmp.get_nvts(extended=True, sort_order="sort_order")

        self.connection.send.has_been_called_with(
            b'<get_nvts sort_order="sort_order"/>'
        )

    def test_get_extended_nvts_with_sort_field(self):
        self.gmp.get_nvts(extended=True, sort_field="sort_field")

        self.connection.send.has_been_called_with(
            b'<get_nvts sort_field="sort_field"/>'
        )
