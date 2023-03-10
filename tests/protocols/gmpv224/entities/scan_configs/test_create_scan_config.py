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


class GmpCreateScanConfigTestMixin:
    def test_create_scan_config(self):
        self.gmp.create_scan_config("a1", "foo")

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<copy>a1</copy>"
            "<name>foo</name>"
            "<usage_type>scan</usage_type>"
            "</create_config>"
        )

    def test_create_scan_config_with_comment(self):
        self.gmp.create_scan_config("a1", "foo", comment="comment")

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<comment>comment</comment>"
            "<copy>a1</copy>"
            "<name>foo</name>"
            "<usage_type>scan</usage_type>"
            "</create_config>"
        )

    def test_create_scan_config_missing_scan_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config(config_id="", name="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config(config_id=None, name="foo")

    def test_create_scan_config_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config(config_id="c1", name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config(config_id="c1", name="")
