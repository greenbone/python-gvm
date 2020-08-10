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

from gvm.errors import RequiredArgument


class GmpCloneTargetCommandTestCase:

    TARGET_ID = '00000000-0000-0000-0000-000000000000'

    def test_clone(self):
        self.gmp.clone_target(self.TARGET_ID)

        self.connection.send.has_been_called_with(
            '<create_target>'
            '<copy>{copy}</copy>'
            '</create_target>'.format(copy=self.TARGET_ID)
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_target('')

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_target(None)


if __name__ == '__main__':
    unittest.main()
