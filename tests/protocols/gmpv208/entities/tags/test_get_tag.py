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


class GmpGetTagTestMixin:
    def test_get_tag(self):
        self.gmp.get_tag("t1")

        self.connection.send.has_been_called_with('<get_tags tag_id="t1"/>')

        self.gmp.get_tag(tag_id="t1")

        self.connection.send.has_been_called_with('<get_tags tag_id="t1"/>')

    def test_get_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_tag(tag_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_tag("")
