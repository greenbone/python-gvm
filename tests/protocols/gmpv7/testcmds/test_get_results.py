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


class GmpGetResultsTestCase:
    def test_get_results(self):
        self.gmp.get_results()

        self.connection.send.has_been_called_with('<get_results/>')

    def test_get_results_with_filter(self):
        self.gmp.get_results(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_results filter="foo=bar"/>'
        )

    def test_get_results_with_filter_id(self):
        self.gmp.get_results(filter_id='f1')

        self.connection.send.has_been_called_with('<get_results filt_id="f1"/>')

    def test_get_results_with_note_details(self):
        self.gmp.get_results(note_details=True)

        self.connection.send.has_been_called_with(
            '<get_results note_details="1"/>'
        )

        self.gmp.get_results(note_details=False)

        self.connection.send.has_been_called_with(
            '<get_results note_details="0"/>'
        )

    def test_get_results_with_override_details(self):
        self.gmp.get_results(override_details=True)

        self.connection.send.has_been_called_with(
            '<get_results override_details="1"/>'
        )

        self.gmp.get_results(override_details=False)

        self.connection.send.has_been_called_with(
            '<get_results override_details="0"/>'
        )

    def test_get_results_with_details(self):
        self.gmp.get_results(details=True)

        self.connection.send.has_been_called_with('<get_results details="1"/>')

        self.gmp.get_results(details=False)

        self.connection.send.has_been_called_with('<get_results details="0"/>')

    def test_get_results_with_task_id(self):
        self.gmp.get_results(task_id='t1')

        self.connection.send.has_been_called_with('<get_results task_id="t1"/>')


if __name__ == '__main__':
    unittest.main()
