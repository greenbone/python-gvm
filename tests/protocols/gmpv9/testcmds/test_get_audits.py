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


class GmpGetAuditsTestCase:
    def test_get_audits_simple(self):
        self.gmp.get_audits()

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit"/>'
        )

    def test_get_audits_with_filter(self):
        self.gmp.get_audits(filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" filter="name=foo"/>'
        )

    def test_get_audits_with_filter_id(self):
        self.gmp.get_audits(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" filt_id="f1"/>'
        )

    def test_get_audits_from_trash(self):
        self.gmp.get_audits(trash=True)

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" trash="1"/>'
        )

    def test_get_audits_with_details(self):
        self.gmp.get_audits(details=True)

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" details="1"/>'
        )

    def test_get_audits_without_details(self):
        self.gmp.get_audits(details=False)

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" details="0"/>'
        )

    def test_get_audits_with_schedules_only(self):
        self.gmp.get_audits(schedules_only=True)

        self.connection.send.has_been_called_with(
            '<get_tasks usage_type="audit" schedules_only="1"/>'
        )


if __name__ == '__main__':
    unittest.main()
