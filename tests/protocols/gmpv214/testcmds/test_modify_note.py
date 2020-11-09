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


class GmpModifyNoteTestCase:
    def test_modify_note(self):
        self.gmp.modify_note(note_id='n1', text='foo')

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">' '<text>foo</text>' '</modify_note>'
        )

    def test_modify_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id=None, text='foo')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id='', text='foo')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note('', text='foo')

    def test_modify_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id='n1', text='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id='n1', text=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note('n1', '')

    def test_modify_note_with_days_active(self):
        self.gmp.modify_note(note_id='n1', text='foo', days_active=0)

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<active>0</active>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', days_active=-1)

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<active>-1</active>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', days_active=600)

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<active>600</active>'
            '</modify_note>'
        )

    def test_modify_note_with_port(self):
        self.gmp.modify_note(note_id='n1', text='foo', port='123')

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<port>123</port>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', port=123)

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<port>123</port>'
            '</modify_note>'
        )

    def test_modify_note_with_hosts(self):
        self.gmp.modify_note(note_id='n1', text='foo', hosts=['foo'])

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<hosts>foo</hosts>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', hosts=['foo', 'bar'])

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<hosts>foo,bar</hosts>'
            '</modify_note>'
        )

    def test_modify_note_with_result_id(self):
        self.gmp.modify_note(note_id='n1', text='foo', result_id='r1')

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<result id="r1"/>'
            '</modify_note>'
        )

    def test_modify_note_with_task_id(self):
        self.gmp.modify_note(note_id='n1', text='foo', task_id='r1')

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<task id="r1"/>'
            '</modify_note>'
        )

    def test_modify_note_with_severity(self):
        self.gmp.modify_note(note_id='n1', text='foo', severity='5.5')

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<severity>5.5</severity>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', severity=5.5)

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<severity>5.5</severity>'
            '</modify_note>'
        )

        self.gmp.modify_note(note_id='n1', text='foo', severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">'
            '<text>foo</text>'
            '<severity>5.5</severity>'
            '</modify_note>'
        )

    def test_modify_note_with_threat(self):
        self.gmp.modify_note(
            note_id='n1', text='foo', threat=SeverityLevel.HIGH
        )

        self.connection.send.has_been_called_with(
            '<modify_note note_id="n1">' '<text>foo</text>' '</modify_note>'
        )


if __name__ == '__main__':
    unittest.main()
