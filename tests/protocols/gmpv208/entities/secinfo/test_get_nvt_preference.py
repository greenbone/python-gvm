# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetNvtPreferenceTestMixin:
    def test_get_preference(self):
        self.gmp.get_nvt_preference(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_preferences preference="foo"/>'
        )

    def test_get_nvt_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt_preference(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt_preference(name="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt_preference("")

    def test_get_nvt_preference_with_nvt_oid(self):
        self.gmp.get_nvt_preference(name="foo", nvt_oid="oid")

        self.connection.send.has_been_called_with(
            b'<get_preferences preference="foo" nvt_oid="oid"/>'
        )
