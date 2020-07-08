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


class GmpGetInfoListTestCase:
    def test_get_info_list(self):
        self.gmp.get_info_list(InfoType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            '<get_info type="CERT_BUND_ADV"/>'
        )

        self.gmp.get_info_list(InfoType.CPE)

        self.connection.send.has_been_called_with('<get_info type="CPE"/>')

        self.gmp.get_info_list(info_type=InfoType.CPE)

        self.connection.send.has_been_called_with('<get_info type="CPE"/>')

        self.gmp.get_info_list(InfoType.CVE)

        self.connection.send.has_been_called_with('<get_info type="CVE"/>')

        self.gmp.get_info_list(InfoType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            '<get_info type="DFN_CERT_ADV"/>'
        )

        self.gmp.get_info_list(InfoType.OVALDEF)

        self.connection.send.has_been_called_with('<get_info type="OVALDEF"/>')

        self.gmp.get_info_list(InfoType.NVT)

        self.connection.send.has_been_called_with('<get_info type="NVT"/>')

        self.gmp.get_info_list(InfoType.ALLINFO)

        self.connection.send.has_been_called_with('<get_info type="ALLINFO"/>')

    def test_get_info_list_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list(info_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list(info_type='')

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list('')

    def test_get_info_list_invalid_info_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_info_list(info_type='foo')

    def test_get_info_list_with_filter(self):
        self.gmp.get_info_list(InfoType.CPE, filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_info type="CPE" filter="foo=bar"/>'
        )

    def test_get_info_list_with_filter_id(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_info type="CPE" filt_id="f1"/>'
        )

    def test_get_info_list_with_name(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, name='foo')

        self.connection.send.has_been_called_with(
            '<get_info type="CPE" name="foo"/>'
        )

    def test_get_info_list_with_details(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, details=True)

        self.connection.send.has_been_called_with(
            '<get_info type="CPE" details="1"/>'
        )

        self.gmp.get_info_list(info_type=InfoType.CPE, details=False)

        self.connection.send.has_been_called_with(
            '<get_info type="CPE" details="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
