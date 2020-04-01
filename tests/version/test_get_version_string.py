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

from gvm.version import get_version_string


class TestGetVersionString(unittest.TestCase):
    def test_simple_version(self):
        self.assertEqual(get_version_string((1, 0)), '1.0')

    def test_release_patch_version(self):
        self.assertEqual(get_version_string((1, 0, 1)), '1.0.1')

    def test_dev_version(self):
        self.assertEqual(get_version_string((1, 0, 1, 'dev', 1)), '1.0.1.dev1')

    def test_beta_version(self):
        self.assertEqual(
            get_version_string((1, 0, 1, 'beta', 1)), '1.0.1.beta1'
        )

    def test_dev_after_beta_version(self):
        self.assertEqual(
            get_version_string((1, 0, 1, 'beta', 2, 'dev', 1)),
            '1.0.1.beta2.dev1',
        )
