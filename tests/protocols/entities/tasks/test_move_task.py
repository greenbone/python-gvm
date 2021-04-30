# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 Greenbone Networks GmbH
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

from gvm.errors import GvmError

from ...gmpv208 import Gmpv208TestCase
from ...gmpv214 import Gmpv214TestCase


class GmpMoveTaskTestCase:
    def test_move_task(self):
        self.gmp.move_task('a1')

        self.connection.send.has_been_called_with('<move_task task_id="a1"/>')

    def test_move_task_to_slave(self):
        self.gmp.move_task('a1', slave_id='s1')

        self.connection.send.has_been_called_with(
            '<move_task task_id="a1" slave_id="s1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.move_task(None)

        with self.assertRaises(GvmError):
            self.gmp.move_task('')


# For new versions add another Mixin here.
class Gmpv208MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv214MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv214TestCase):
    pass
