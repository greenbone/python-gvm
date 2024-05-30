# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetCpeListTestMixin:
    def test_get_cpes(self):
        self.gmp.get_cpes()

        self.connection.send.has_been_called_with(b'<get_info type="CPE"/>')

    def test_get_cpes_with_filter_string(self):
        self.gmp.get_cpes(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" filter="foo=bar"/>'
        )

    def test_get_cpes_with_filter_id(self):
        self.gmp.get_cpes(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" filt_id="f1"/>'
        )

    def test_get_cpes_with_name(self):
        self.gmp.get_cpes(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" name="foo"/>'
        )

    def test_get_cpes_with_details(self):
        self.gmp.get_cpes(details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" details="1"/>'
        )

        self.gmp.get_cpes(details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" details="0"/>'
        )
