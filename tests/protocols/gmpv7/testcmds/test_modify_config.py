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
import warnings

from gvm.errors import RequiredArgument, InvalidArgument


class GmpModifyConfigTestCase:
    def test_modify_config_invalid_selection(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_config(config_id='c1', selection='foo')

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_config(config_id='c1', selection='')

    def test_modify_config_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config(config_id=None, selection='nvt_pref')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config(config_id='', selection='nvt_pref')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config('', selection='nvt_pref')

    def test_modify_config_set_comment(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_config(
                config_id='c1', selection=None, comment='foo'
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<comment>foo</comment>'
            '</modify_config>'
        )

    def test_modify_config_set_nvt_pref(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_config(
                config_id='c1', selection='nvt_pref', nvt_oid='o1', name='foo'
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<nvt oid="o1"/>'
            '<name>foo</name>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_set_scanner_pref(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_config(
                config_id='c1', selection='scan_pref', name='foo', value='bar'
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<name>foo</name>'
            '<value>YmFy</value>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_set_nvt_selection(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_config(
                config_id='c1',
                selection='nvt_selection',
                nvt_oids=['o1'],
                family='foo',
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '<nvt oid="o1"/>'
            '</nvt_selection>'
            '</modify_config>'
        )

    def test_modify_config_set_family_selection(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_config(
                config_id='c1', selection='family_selection', families=['foo']
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<family_selection>'
            '<growing>1</growing>'
            '<family>'
            '<name>foo</name>'
            '<all>1</all>'
            '<growing>1</growing>'
            '</family>'
            '</family_selection>'
            '</modify_config>'
        )


if __name__ == '__main__':
    unittest.main()
