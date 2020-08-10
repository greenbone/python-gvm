# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import unittest

from gvm.errors import InvalidArgument


class GmpHelpTestCase:
    def test_help(self):
        self.gmp.help()

        self.connection.send.has_been_called_with('<help type=""/>')

    def test_invalid_help_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.help(help_type='foo')

    def test_help_type_brief(self):
        self.gmp.help(help_type='brief')

        self.connection.send.has_been_called_with('<help type="brief"/>')

    def test_invalid_format(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.help(format='foo')

    def test_html_format(self):
        self.gmp.help(format='html')

        self.connection.send.has_been_called_with(
            '<help type="" format="html"/>'
        )


if __name__ == '__main__':
    unittest.main()
