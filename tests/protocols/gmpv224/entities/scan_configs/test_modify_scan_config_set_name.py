# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 Greenbone AG
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


class GmpModifyScanConfigSetNameTestMixin:
    def test_modify_scan_config_set_name(self):
        self.gmp.modify_scan_config_set_name("c1", "foo")

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<name>foo</name>"
            "</modify_config>"
        )

    def test_modify_scan_config_set_name_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name(config_id=None, name="name")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name("", name="name")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name(config_id="", name="name")

    def test_modify_scan_config_set_name_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name(config_id="c", name="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name(config_id="c", name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_name("c", "")
