# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetOverridesTestMixin:
    def test_get_overrides(self):
        self.gmp.get_overrides()

        self.connection.send.has_been_called_with(b"<get_overrides/>")

    def test_get_overrides_with_filter_string(self):
        self.gmp.get_overrides(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_overrides filter="foo=bar"/>'
        )

    def test_get_overrides_with_filter_id(self):
        self.gmp.get_overrides(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_overrides filt_id="f1"/>'
        )

    def test_get_overrides_with_details(self):
        self.gmp.get_overrides(details=True)

        self.connection.send.has_been_called_with(
            b'<get_overrides details="1"/>'
        )

        self.gmp.get_overrides(details=False)

        self.connection.send.has_been_called_with(
            b'<get_overrides details="0"/>'
        )

    def test_get_overrides_with_result(self):
        self.gmp.get_overrides(result=True)

        self.connection.send.has_been_called_with(
            b'<get_overrides result="1"/>'
        )

        self.gmp.get_overrides(result=False)

        self.connection.send.has_been_called_with(
            b'<get_overrides result="0"/>'
        )
