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


class GmpCloneAgentTestCase:
    def test_deprecation_create_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.create_agent(
                installer='foo', signature='bar', name='ipsum', comment='lorem'
            )

    def test_deprecation_clone_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.clone_agent('a1')

    def test_deprecation_delete_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.delete_agent('a1')

    def test_deprecation_modify_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.modify_agent('a1')

    def test_deprecation_verify_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.verify_agent('a1')

    def test_deprecation_get_agent(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.get_agent('a1')


if __name__ == '__main__':
    unittest.main()
