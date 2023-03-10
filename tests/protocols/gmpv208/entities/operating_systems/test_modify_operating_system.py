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


class GmpModifyOperatingSystemTestMixin:
    def test_modify_operating_system(self):
        self.gmp.modify_operating_system(operating_system_id="a1")

        self.connection.send.has_been_called_with(
            '<modify_asset asset_id="a1">'
            "<comment></comment>"
            "</modify_asset>"
        )

    def test_modify_operating_system_without_operating_system_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_operating_system(
                operating_system_id=None, comment="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_operating_system(
                operating_system_id="", comment="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_operating_system("", comment="foo")

    def test_modify_operating_system_with_comment(self):
        self.gmp.modify_operating_system("a1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_asset asset_id="a1">'
            "<comment>foo</comment>"
            "</modify_asset>"
        )

        self.gmp.modify_operating_system("a1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_asset asset_id="a1">'
            "<comment>foo</comment>"
            "</modify_asset>"
        )

        self.gmp.modify_operating_system("a1", comment="")

        self.connection.send.has_been_called_with(
            '<modify_asset asset_id="a1">'
            "<comment></comment>"
            "</modify_asset>"
        )

        self.gmp.modify_operating_system("a1", comment=None)

        self.connection.send.has_been_called_with(
            '<modify_asset asset_id="a1">'
            "<comment></comment>"
            "</modify_asset>"
        )
