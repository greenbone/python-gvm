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


class GmpGetOvalDefListTestMixin:
    def test_get_oval_definitions(self):
        self.gmp.get_oval_definitions()

        self.connection.send.has_been_called_with('<get_info type="OVALDEF"/>')

    def test_get_oval_definitions_with_filter_string(self):
        self.gmp.get_oval_definitions(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            '<get_info type="OVALDEF" filter="foo=bar"/>'
        )

    def test_get_oval_definitions_with_filter_id(self):
        self.gmp.get_oval_definitions(filter_id="f1")

        self.connection.send.has_been_called_with(
            '<get_info type="OVALDEF" filt_id="f1"/>'
        )

    def test_get_oval_definitions_with_name(self):
        self.gmp.get_oval_definitions(name="foo")

        self.connection.send.has_been_called_with(
            '<get_info type="OVALDEF" name="foo"/>'
        )

    def test_get_oval_definitions_with_details(self):
        self.gmp.get_oval_definitions(details=True)

        self.connection.send.has_been_called_with(
            '<get_info type="OVALDEF" details="1"/>'
        )

        self.gmp.get_oval_definitions(details=False)

        self.connection.send.has_been_called_with(
            '<get_info type="OVALDEF" details="0"/>'
        )
