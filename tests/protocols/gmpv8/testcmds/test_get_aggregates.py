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

from gvm.errors import RequiredArgument, InvalidArgumentType

from gvm.protocols.gmpv8 import EntityType


class GmpGetAggregatesTestCase:
    def test_get_aggregates(self):
        self.gmp.get_aggregates(EntityType.ALERT)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="alert"/>'
        )

        self.gmp.get_aggregates(resource_type=EntityType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cert_bund_adv"/>'
        )

        self.gmp.get_aggregates(EntityType.CPE)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cpe"/>'
        )

        self.gmp.get_aggregates(EntityType.CVE)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="cve"/>'
        )

        self.gmp.get_aggregates(EntityType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="dfn_cert_adv"/>'
        )

        self.gmp.get_aggregates(EntityType.HOST)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="host"/>'
        )

        self.gmp.get_aggregates(EntityType.NOTE)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="note"/>'
        )

        self.gmp.get_aggregates(EntityType.NVT)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="nvt"/>'
        )

        self.gmp.get_aggregates(EntityType.OPERATING_SYSTEM)

        self.connection.send.has_been_called_with('<get_aggregates type="os"/>')

        self.gmp.get_aggregates(EntityType.OVALDEF)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="ovaldef"/>'
        )

        self.gmp.get_aggregates(EntityType.OVERRIDE)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="override"/>'
        )

        self.gmp.get_aggregates(EntityType.REPORT)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="report"/>'
        )

        self.gmp.get_aggregates(EntityType.RESULT)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="result"/>'
        )

        self.gmp.get_aggregates(EntityType.TASK)

        self.connection.send.has_been_called_with(
            '<get_aggregates type="task"/>'
        )

    def test_get_aggregates_kwargs(self):
        self.gmp.get_aggregates(EntityType.ALERT, group_column="family")

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
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_aggregates(resource_type='foo')


if __name__ == '__main__':
    unittest.main()
