# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gvm.errors import RequiredArgument


class GmpGetOvalDefTestMixin:
    def test_get_oval_definition(self):
        self.gmp.get_oval_definition(oval_id="i1")

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

        self.gmp.get_oval_definition("i1")

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

    def test_get_oval_definition_missing_oval_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition(oval_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_oval_definition(oval_id=None)
