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
import warnings

from gvm.utils import deprecation


class TestDeprecation(unittest.TestCase):
    def test_deprecation(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            self.assertEqual(len(w), 0)

            warnings.simplefilter("always")

            deprecation('I am deprecated')

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn(str(w[0].message), 'I am deprecated')


if __name__ == '__main__':
    unittest.main()
