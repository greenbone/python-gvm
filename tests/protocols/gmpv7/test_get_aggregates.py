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

from gvm.errors import RequiredArgument, InvalidArgument

from . import Gmpv7TestCase


class GmpGetAggregatesTestCase(Gmpv7TestCase):
    def test_get_aggregates(self):
        self.gmp.get_aggregates('alert')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="alert"/>'
        )

        self.gmp.get_aggregates('allinfo')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="allinfo"/>'
        )

        self.gmp.get_aggregates(resource_type='cert_bund_adv')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cert_bund_adv"/>'
        )

        self.gmp.get_aggregates('cpe')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cpe"/>'
        )

        self.gmp.get_aggregates('cve')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cve"/>'
        )

        self.gmp.get_aggregates('dfn_cert_adv')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="dfn_cert_adv"/>'
        )

        self.gmp.get_aggregates('host')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="host"/>'
        )

        self.gmp.get_aggregates('note')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="note"/>'
        )

        self.gmp.get_aggregates('nvt')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="nvt"/>'
        )

        self.gmp.get_aggregates('os')

        self.connection.send.has_been_called_with('<get_aggregates type="os"/>')

        self.gmp.get_aggregates('ovaldef')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="ovaldef"/>'
        )

        self.gmp.get_aggregates('override')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="override"/>'
        )

        self.gmp.get_aggregates('report')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="report"/>'
        )

        self.gmp.get_aggregates('result')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="result"/>'
        )

        self.gmp.get_aggregates('task')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="task"/>'
        )

        self.gmp.get_aggregates('vuln')

        self.connection.send.has_been_called_with(
            '<get_aggregates type="vuln"/>'
        )

    def test_get_aggregates_kwargs(self):
        self.gmp.get_aggregates('alert', group_column="family")

        self.connection.send.has_been_called_with(
            '<get_aggregates type="alert" group_column="family"/>'
        )

    def test_get_aggregates_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(resource_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(resource_type='')

        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates('')

    def test_get_aggregates_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_aggregates(resource_type='foo')


if __name__ == '__main__':
    unittest.main()
