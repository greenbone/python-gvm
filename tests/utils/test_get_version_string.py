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

from gvm.utils import get_version_string

class TestGetVersionString(unittest.TestCase):

    def test_simple_version(self):
        self.assertEqual(get_version_string((1, 0)), '1.0')

    def test_release_patch_version(self):
        self.assertEqual(get_version_string((1, 0, 1)), '1.0.1')

    def test_dev_version(self):
        self.assertEqual(get_version_string((1, 0, 1, 'dev', 1)), '1.0.1.dev1')

    def test_beta_version(self):
        self.assertEqual(
            get_version_string((1, 0, 1, 'beta', 1)), '1.0.1beta1')

    def test_dev_after_beta_version(self):
        self.assertEqual(get_version_string((1, 0, 1, 'beta', 2, 'dev', 1)),
                         '1.0.1beta2.dev1')

    def test_pep440_pre_release_versions(self):
        self.assertEqual(
            get_version_string((1, 0, 1, 'beta', 1)), '1.0.1beta1')
        self.assertEqual(
            get_version_string((1, 0, 1, 'b', 1)), '1.0.1b1')
        self.assertEqual(
            get_version_string((1, 0, 1, 'alpha', 1)), '1.0.1alpha1')
        self.assertEqual(
            get_version_string((1, 0, 1, 'a', 1)), '1.0.1a1')
        self.assertEqual(
            get_version_string((1, 0, 1, 'pre', 1)), '1.0.1pre1')
        self.assertEqual(
            get_version_string((1, 0, 1, 'rc', 1)), '1.0.1rc1')


if __name__ == '__main__':
    unittest.main()
