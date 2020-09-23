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
from gvm.protocols.gmpv9 import ScannerType


class GmpModifyScannerTestCase:
    def test_modify_scanner(self):
        self.gmp.modify_scanner(scanner_id='s1')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1"/>'
        )

    def test_modify_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scanner(scanner_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scanner(scanner_id='')

    def test_modify_scanner_with_comment(self):
        self.gmp.modify_scanner(scanner_id='s1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<comment>foo</comment>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_host(self):
        self.gmp.modify_scanner(scanner_id='s1', host='foo')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<host>foo</host>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_port(self):
        self.gmp.modify_scanner(scanner_id='s1', port=1234)

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<port>1234</port>'
            '</modify_scanner>'
        )

        self.gmp.modify_scanner(scanner_id='s1', port='1234')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<port>1234</port>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_name(self):
        self.gmp.modify_scanner(scanner_id='s1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<name>foo</name>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_ca_pub(self):
        self.gmp.modify_scanner(scanner_id='s1', ca_pub='foo')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<ca_pub>foo</ca_pub>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_credential_id(self):
        self.gmp.modify_scanner(scanner_id='s1', credential_id='c1')

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<credential id="c1"/>'
            '</modify_scanner>'
        )

    def test_modify_scanner_with_scanner_type(self):
        self.gmp.modify_scanner(
            scanner_id='s1', scanner_type=ScannerType.OSP_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<type>1</type>'
            '</modify_scanner>'
        )

        self.gmp.modify_scanner(
            scanner_id='s1', scanner_type=ScannerType.OPENVAS_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<type>2</type>'
            '</modify_scanner>'
        )

        self.gmp.modify_scanner(
            scanner_id='s1', scanner_type=ScannerType.CVE_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<type>3</type>'
            '</modify_scanner>'
        )

        self.gmp.modify_scanner(
            scanner_id='s1', scanner_type=ScannerType.GMP_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            '<modify_scanner scanner_id="s1">'
            '<type>4</type>'
            '</modify_scanner>'
        )

    def test_modify_scanner_invalid_scanner_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_scanner(scanner_id='s1', scanner_type='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_scanner(scanner_id='s1', scanner_type='-1')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_scanner(scanner_id='s1', scanner_type=1)


if __name__ == '__main__':
    unittest.main()
