# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 Greenbone Networks GmbH
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

from gvm.errors import InvalidArgumentType, InvalidArgument


class GmpModifyConfigTestCase:
    def test_modify_config(self):
        self.gmp.modify_config(
            config_id='c1',
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1"/>'
        )
        self.gmp.modify_config(
            'c1',
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1"/>'
        )

    def test_modify_config_name_and_comment(self):
        self.gmp.modify_config(
            config_id='c1',
            name='foo',
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<name>foo</name>'
            '</modify_config>'
        )
        self.gmp.modify_config(
            config_id='c1',
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<comment>bar</comment>'
            '</modify_config>'
        )
        self.gmp.modify_config(
            config_id='c1',
            name='foo',
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<name>foo</name>'
            '<comment>bar</comment>'
            '</modify_config>'
        )

    def test_modify_config_modify_scanner_preferences(self):
        self.gmp.modify_config(
            config_id='c1',
            scanner_preferences=[
                ('a', '0'),
                ('b', '110')
            ],
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference><name>a</name><value>MA==</value></preference>'
            '<preference><name>b</name><value>MTEw</value></preference>'
            '</modify_config>'
        )


        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_config(
                config_id='c1',
                scanner_preferences='foo',
            )

    def test_modify_config_modify_nvt_preferences(self):
        self.gmp.modify_config(
            config_id='c1',
            nvt_preferences=[
                (
                    '1.2.3:1:entry:foo',
                    'foo',
                    'bar'
                ),
                (
                    '1.2.3.4:10:checkbox:baz',
                    'baz',
                    'yyzyy'
                ),
            ],
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference><nvt oid="1.2.3:1:entry:foo"/><name>foo</name>'
            '<value>YmFy</value></preference>'
            '<preference><nvt oid="1.2.3.4:10:checkbox:baz"/>'
            '<name>baz</name><value>eXl6eXk=</value></preference>'
            '</modify_config>'
        )


        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_config(
                config_id='c1',
                nvt_preferences='foo',
            )

    def test_modify_config_add_nvts(self):
        self.gmp.modify_config(
            config_id='c1',
            nvts=[(
                "fam_sec",
                ['a', 'b']
            )],
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection><family>fam_sec</family><nvt oid="a"/>'
            '<nvt oid="b"/></nvt_selection>'
            '</modify_config>'
        )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_config(
                config_id='c1',
                nvts=[(
                    "fam_sec",
                    'a'
                )],

            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_config(
                config_id='c1',
                nvts='foo',
            )

    def test_modify_config_add_nvt_families(self):
        self.gmp.modify_config(
            config_id='c1',
            nvt_families=[('family', True, True)]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<family_selection><growing>1</growing><family><name>family</name>'
            '<all>1</all><growing>1</growing></family></family_selection>'
            '</modify_config>'
        )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_config(
                config_id='c1',
                nvt_families='foo',
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_config(
                config_id='c1',
                nvt_families=[('family', True)]
            )

    def test_modify_config_complex_call(self):
        self.gmp.modify_config(
            config_id='c1',
            name='config',
            comment="bello",
            scanner_preferences=[
                ('a', '0'),
                ('b', '110')
            ],
            nvt_preferences=[
                (
                    '1.2.3:1:entry:foo',
                    'foo',
                    'bar'
                ),
                (
                    '1.2.3.4:10:checkbox:baz',
                    'baz',
                    'yyzyy'
                ),
            ],
            nvts=[(
                "fam_sec",
                ['a', 'b']
            )],
            nvt_families=[('family', True, True)]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<name>config</name><comment>bello</comment>'
            '<preference><name>a</name><value>MA==</value></preference>'
            '<preference><name>b</name><value>MTEw</value></preference>'
            '<preference><nvt oid="1.2.3:1:entry:foo"/><name>foo</name>'
            '<value>YmFy</value></preference>'
            '<preference><nvt oid="1.2.3.4:10:checkbox:baz"/>'
            '<name>baz</name><value>eXl6eXk=</value></preference>'
            '<nvt_selection><family>fam_sec</family><nvt oid="a"/>'
            '<nvt oid="b"/></nvt_selection>'
            '<family_selection><growing>1</growing><family><name>family</name>'
            '<all>1</all><growing>1</growing></family></family_selection>'
            '</modify_config>'
        )


if __name__ == '__main__':
    unittest.main()
