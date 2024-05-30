# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetOvalDefTestMixin:
    def test_get_oval_definition(self):
        self.gmp.get_oval_definition(oval_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

        self.gmp.get_oval_definition("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

    def test_get_oval_definition_missing_oval_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition(oval_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition(oval_id=None)
