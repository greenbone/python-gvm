# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetFiltersTestMixin:
    def test_get_filters(self):
        self.gmp.get_filters()

        self.connection.send.has_been_called_with(b"<get_filters/>")

    def test_get_filters_with_filter_string(self):
        self.gmp.get_filters(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_filters filter="foo=bar"/>'
        )

    def test_get_filters_with_filter_id(self):
        self.gmp.get_filters(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_filters filt_id="f1"/>'
        )

    def test_get_filters_with_trash(self):
        self.gmp.get_filters(trash=True)

        self.connection.send.has_been_called_with(b'<get_filters trash="1"/>')

        self.gmp.get_filters(trash=False)

        self.connection.send.has_been_called_with(b'<get_filters trash="0"/>')

    def test_get_filters_with_alerts(self):
        self.gmp.get_filters(alerts=True)

        self.connection.send.has_been_called_with(b'<get_filters alerts="1"/>')

        self.gmp.get_filters(alerts=False)

        self.connection.send.has_been_called_with(b'<get_filters alerts="0"/>')
