# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetOverrideTestMixin:
    def test_get_override(self):
        self.gmp.get_override("o1")

        self.connection.send.has_been_called_with(
            b'<get_overrides override_id="o1" details="1"/>'
        )

        self.gmp.get_override(override_id="o1")

        self.connection.send.has_been_called_with(
            b'<get_overrides override_id="o1" details="1"/>'
        )

    def test_get_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_override(override_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_override("")
