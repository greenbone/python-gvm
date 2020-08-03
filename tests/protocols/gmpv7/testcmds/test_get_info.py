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

from gvm.protocols.gmpv7 import InfoType


class GmpGetInfoTestCase:
    def test_get_info(self):
        self.gmp.get_info(info_type=InfoType.CERT_BUND_ADV, info_id='i1')

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.CPE)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="CPE" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.CVE)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="CVE" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="DFN_CERT_ADV" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.OVALDEF)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.NVT)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="NVT" details="1"/>'
        )

        self.gmp.get_info('i1', InfoType.ALLINFO)

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="ALLINFO" details="1"/>'
        )

    def test_get_info_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id='i1', info_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id='i1', info_type='')

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info('i1', '')

    def test_get_info_invalid_info_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_info(info_id='i1', info_type='foo')

    def test_get_info_missing_info_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id='', info_type=InfoType.CPE)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info('', info_type=InfoType.CPE)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id=None, info_type=InfoType.CPE)


if __name__ == '__main__':
    unittest.main()
