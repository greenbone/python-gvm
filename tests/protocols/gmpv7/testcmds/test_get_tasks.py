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


class GmpGetTasksTestCase:
    def test_get_tasks_simple(self):
        self.gmp.get_tasks()

        self.connection.send.has_been_called_with('<get_tasks/>')

    def test_get_tasks_with_filter(self):
        self.gmp.get_tasks(filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_tasks filter="name=foo"/>'
        )

    def test_get_tasks_with_filter_id(self):
        self.gmp.get_tasks(filter_id='f1')

        self.connection.send.has_been_called_with('<get_tasks filt_id="f1"/>')

    def test_get_tasks_from_trash(self):
        self.gmp.get_tasks(trash=True)

        self.connection.send.has_been_called_with('<get_tasks trash="1"/>')

    def test_get_tasks_with_details(self):
        self.gmp.get_tasks(details=True)

        self.connection.send.has_been_called_with('<get_tasks details="1"/>')

    def test_get_tasks_without_details(self):
        self.gmp.get_tasks(details=False)

        self.connection.send.has_been_called_with('<get_tasks details="0"/>')

    def test_get_tasks_with_schedules_only(self):
        self.gmp.get_tasks(schedules_only=True)

        self.connection.send.has_been_called_with(
            '<get_tasks schedules_only="1"/>'
        )


if __name__ == '__main__':
    unittest.main()
