# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from gvm.version import check_version_equal


class CheckVersionEqualTestCase(unittest.TestCase):
    def test_version_equal(self):
        self.assertTrue(check_version_equal('1.2.3', '1.2.3'))
        self.assertTrue(check_version_equal('1.2.3a', '1.2.3a0'))
        self.assertTrue(check_version_equal('1.2.3a0', '1.2.3.a0'))
        self.assertTrue(check_version_equal('1.2.3dev1', '1.2.3.dev1'))

    def test_version_not_equal(self):
        self.assertFalse(check_version_equal('1.2.3', '1.2'))
        self.assertFalse(check_version_equal('1.2.3a', '1.2.3a1'))
        self.assertFalse(check_version_equal('1.2.3a0', '1.2.3.a1'))
        self.assertFalse(check_version_equal('1.2.3dev', '1.2.3dev1'))
        self.assertFalse(check_version_equal('1.2.3dev', '1.2.3.dev1'))
        self.assertFalse(check_version_equal('1.2.3.dev1', '1.2.3.dev2'))
