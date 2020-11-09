# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from decimal import Decimal

from gvm.errors import RequiredArgument

from gvm.protocols.gmpv214 import SeverityLevel


class GmpCreateNoteTestCase:
    def test_create_note(self):
        self.gmp.create_note('foo', nvt_oid='oid1')

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '</create_note>'
        )

    def test_create_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_note(None, 'od1')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_note('', 'oid1')

    def test_create_note_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_note('foo', None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_note('foo', '')

    def test_create_note_with_hosts(self):
        self.gmp.create_note('foo', nvt_oid='oid1', hosts=[])

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', hosts=['h1', 'h2'])

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<hosts>h1,h2</hosts>'
            '</create_note>'
        )

    def test_create_note_with_port(self):
        self.gmp.create_note('foo', nvt_oid='oid1', port='666')

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<port>666</port>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', port=666)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<port>666</port>'
            '</create_note>'
        )

    def test_create_note_with_result_id(self):
        self.gmp.create_note('foo', nvt_oid='oid1', result_id='r1')

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<result id="r1"/>'
            '</create_note>'
        )

    def test_create_note_with_task_id(self):
        self.gmp.create_note('foo', nvt_oid='oid1', task_id='t1')

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<task id="t1"/>'
            '</create_note>'
        )

    def test_create_note_with_severity(self):
        self.gmp.create_note('foo', nvt_oid='oid1', severity='5.5')

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<severity>5.5</severity>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', severity=5.5)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<severity>5.5</severity>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<severity>5.5</severity>'
            '</create_note>'
        )

    def test_create_note_with_threat(self):
        self.gmp.create_note('foo', nvt_oid='oid1', threat=SeverityLevel.HIGH)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '</create_note>'
        )

    def test_create_note_with_days_active(self):
        self.gmp.create_note('foo', nvt_oid='oid1', days_active=0)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<active>0</active>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', days_active=-1)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<active>-1</active>'
            '</create_note>'
        )

        self.gmp.create_note('foo', nvt_oid='oid1', days_active=3600)

        self.connection.send.has_been_called_with(
            '<create_note>'
            '<text>foo</text>'
            '<nvt oid="oid1"/>'
            '<active>3600</active>'
            '</create_note>'
        )


if __name__ == '__main__':
    unittest.main()
