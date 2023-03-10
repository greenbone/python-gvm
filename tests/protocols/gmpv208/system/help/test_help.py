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

from gvm.errors import InvalidArgumentType
from gvm.protocols.gmpv208 import HelpFormat


class GmpHelpTestMixin:
    def test_help(self):
        self.gmp.help()

        self.connection.send.has_been_called_with('<help type=""/>')

    def test_help_type_brief(self):
        self.gmp.help(brief=True)

        self.connection.send.has_been_called_with('<help type="brief"/>')

    def test_invalid_help_format(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.help(help_format="foo")

    def test_html_format(self):
        self.gmp.help(help_format=HelpFormat.HTML)

        self.connection.send.has_been_called_with(
            '<help type="" format="html"/>'
        )
