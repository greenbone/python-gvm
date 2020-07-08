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

from gvm.protocols.gmpv7 import ScannerType


class GmpCreateScannerTestCase:
    def test_create_scanner(self):
        self.gmp.create_scanner(
            name='foo',
            host='localhost',
            port=1234,
            scanner_type=ScannerType.OSP_SCANNER_TYPE,
            credential_id='c1',
        )

        self.connection.send.has_been_called_with(
            '<create_scanner>'
            '<name>foo</name>'
            '<host>localhost</host>'
            '<port>1234</port>'
            '<type>1</type>'
            '<credential id="c1"/>'
            '</create_scanner>'
        )

    def test_create_scanner_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name=None,
                host='localhost',
                port=1234,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='c1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='',
                host='localhost',
                port=1234,
                scanner_type='1',
                credential_id='c1',
            )

    def test_create_scanner_missing_host(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host=None,
                port=1234,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='c1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='',
                port=1234,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='c1',
            )

    def test_create_scanner_missing_port(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=None,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='c1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port='',
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='c1',
            )

    def test_create_scanner_missing_scanner_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type=None,
                credential_id='c1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type='',
                credential_id='c1',
            )

    def test_create_scanner_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type=ScannerType.OSP_SCANNER_TYPE,
                credential_id='',
            )

    def test_create_scanner_invalid_scanner_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type='bar',
                credential_id='c1',
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_scanner(
                name='foo',
                host='localhost',
                port=1234,
                scanner_type='55',
                credential_id='c1',
            )

    def test_create_scanner_with_ca_pub(self):
        self.gmp.create_scanner(
            name='foo',
            host='localhost',
            port=1234,
            ca_pub='foo',
            scanner_type=ScannerType.OSP_SCANNER_TYPE,
            credential_id='c1',
        )

        self.connection.send.has_been_called_with(
            '<create_scanner>'
            '<name>foo</name>'
            '<host>localhost</host>'
            '<port>1234</port>'
            '<type>1</type>'
            '<ca_pub>foo</ca_pub>'
            '<credential id="c1"/>'
            '</create_scanner>'
        )

    def test_create_scanner_with_comment(self):
        self.gmp.create_scanner(
            name='foo',
            host='localhost',
            port=1234,
            scanner_type=ScannerType.OSP_SCANNER_TYPE,
            credential_id='c1',
            comment='bar',
        )

        self.connection.send.has_been_called_with(
            '<create_scanner>'
            '<name>foo</name>'
            '<host>localhost</host>'
            '<port>1234</port>'
            '<type>1</type>'
            '<credential id="c1"/>'
            '<comment>bar</comment>'
            '</create_scanner>'
        )


if __name__ == '__main__':
    unittest.main()
