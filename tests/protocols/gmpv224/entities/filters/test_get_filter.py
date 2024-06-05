# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetFilterTestMixin:
    def test_get_filter(self):
        self.gmp.get_filter("f1")

        self.connection.send.has_been_called_with(
            b'<get_filters filter_id="f1"/>'
        )

        self.gmp.get_filter(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_filters filter_id="f1"/>'
        )

    def test_get_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_filter(filter_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_filter("")

    def test_get_filter_with_alerts(self):
        self.gmp.get_filter(filter_id="f1", alerts=True)

        self.connection.send.has_been_called_with(
            b'<get_filters filter_id="f1" alerts="1"/>'
        )

        self.gmp.get_filter(filter_id="f1", alerts=False)

        self.connection.send.has_been_called_with(
            b'<get_filters filter_id="f1" alerts="0"/>'
        )
