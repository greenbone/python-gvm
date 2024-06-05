# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetOvalDefListTestMixin:
    def test_get_oval_definitions(self):
        self.gmp.get_oval_definitions()

        self.connection.send.has_been_called_with(b'<get_info type="OVALDEF"/>')

    def test_get_oval_definitions_with_filter_string(self):
        self.gmp.get_oval_definitions(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="OVALDEF" filter="foo=bar"/>'
        )

    def test_get_oval_definitions_with_filter_id(self):
        self.gmp.get_oval_definitions(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="OVALDEF" filt_id="f1"/>'
        )

    def test_get_oval_definitions_with_name(self):
        self.gmp.get_oval_definitions(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="OVALDEF" name="foo"/>'
        )

    def test_get_oval_definitions_with_details(self):
        self.gmp.get_oval_definitions(details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="OVALDEF" details="1"/>'
        )

        self.gmp.get_oval_definitions(details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="OVALDEF" details="0"/>'
        )
