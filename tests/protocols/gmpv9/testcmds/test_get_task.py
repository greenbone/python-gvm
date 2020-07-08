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


class GmpGetTaskTestCase:
    def test_get_task(self):
        self.gmp.get_task('a1')

        self.connection.send.has_been_called_with(
            '<get_tasks task_id="a1" usage_type="scan" details="1"/>'
        )

    def test_fail_without_task_id(self):
        with self.assertRaises(GvmError):
            self.gmp.get_task(None)

        with self.assertRaises(GvmError):
            self.gmp.get_task('')


if __name__ == '__main__':
    unittest.main()
