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


class GmpGetPoliciesTestCase:
    def test_get_policies_simple(self):
        self.gmp.get_policies()

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy"/>'
        )

    def test_get_policies_with_filter(self):
        self.gmp.get_policies(filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" filter="name=foo"/>'
        )

    def test_get_policies_with_filter_id(self):
        self.gmp.get_policies(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" filt_id="f1"/>'
        )

    def test_get_policies_from_trash(self):
        self.gmp.get_policies(trash=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" trash="1"/>'
        )

    def test_get_policies_with_details(self):
        self.gmp.get_policies(details=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" details="1"/>'
        )

    def test_get_policies_without_details(self):
        self.gmp.get_policies(details=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" details="0"/>'
        )

    def test_get_policies_with_families(self):
        self.gmp.get_policies(families=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" families="1"/>'
        )

    def test_get_policies_without_families(self):
        self.gmp.get_policies(families=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" families="0"/>'
        )

    def test_get_policies_with_preferences(self):
        self.gmp.get_policies(preferences=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" preferences="1"/>'
        )

    def test_get_policies_without_preferences(self):
        self.gmp.get_policies(preferences=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" preferences="0"/>'
        )

    def test_get_policies_with_audits(self):
        self.gmp.get_policies(audits=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" tasks="1"/>'
        )

    def test_get_policies_without_audits(self):
        self.gmp.get_policies(audits=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="policy" tasks="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
