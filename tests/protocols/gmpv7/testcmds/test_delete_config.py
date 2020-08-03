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

from gvm.errors import GvmError


class GmpDeleteConfigTestCase:
    def test_delete(self):
        self.gmp.delete_config('a1')

        self.connection.send.has_been_called_with(
            '<delete_config config_id="a1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_config('a1', ultimate=True)

        self.connection.send.has_been_called_with(
            '<delete_config config_id="a1" ultimate="1"/>'
        )

    def test_missing_config_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_config(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_config('')


if __name__ == '__main__':
    unittest.main()
