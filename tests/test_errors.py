# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.errors import (
    InvalidArgument,
    InvalidArgumentType,
    RequiredArgument,
    GvmError,
    GvmServerError,
    GvmResponseError,
)


class InvalidArgumentTestCase(unittest.TestCase):
    def test_raise_with_message(self):
        with self.assertRaisesRegex(InvalidArgument, '^foo bar$'):
            raise InvalidArgument('foo bar')

    def test_message_precedence(self):
        with self.assertRaisesRegex(InvalidArgument, '^foo bar$') as cm:
            raise InvalidArgument('foo bar', argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertEqual(ex.function, 'bar')

        self.assertEqual(str(ex), 'foo bar')

    def test_raise_with_argument(self):
        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(argument='foo')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertIsNone(ex.function)

    def test_raise_with_function(self):
        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(function='foo')

        ex = cm.exception
        self.assertEqual(ex.function, 'foo')
        self.assertIsNone(ex.argument)

    def test_raise_with_argument_and_function(self):
        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertEqual(ex.function, 'bar')

    def test_string_conversion(self):
        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument('foo bar', argument='foo')

        ex = cm.exception
        self.assertEqual(str(ex), 'foo bar')

        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(argument='foo')

        ex = cm.exception
        self.assertEqual(str(ex), 'Invalid argument foo')

        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(function='foo')

        ex = cm.exception
        self.assertEqual(str(ex), 'Invalid argument for foo')

        with self.assertRaises(InvalidArgument) as cm:
            raise InvalidArgument(argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(str(ex), 'Invalid argument foo for bar')

    def test_is_gvm_error(self):
        with self.assertRaises(GvmError):
            raise InvalidArgument('foo bar')


class RequiredArgumentTestCase(unittest.TestCase):
    def test_raise_with_message(self):
        with self.assertRaisesRegex(RequiredArgument, '^foo bar$'):
            raise RequiredArgument('foo bar')

    def test_message_precedence(self):
        with self.assertRaisesRegex(RequiredArgument, '^foo bar$') as cm:
            raise RequiredArgument('foo bar', argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertEqual(ex.function, 'bar')

        self.assertEqual(str(ex), 'foo bar')

    def test_raise_with_argument(self):
        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(argument='foo')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertIsNone(ex.function)

    def test_raise_with_function(self):
        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(function='foo')

        ex = cm.exception
        self.assertEqual(ex.function, 'foo')
        self.assertIsNone(ex.argument)

    def test_raise_with_argument_and_function(self):
        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(ex.argument, 'foo')
        self.assertEqual(ex.function, 'bar')

    def test_string_conversion(self):
        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument('foo bar')

        ex = cm.exception
        self.assertEqual(str(ex), 'foo bar')

        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(argument='foo')

        ex = cm.exception
        self.assertEqual(str(ex), 'Required argument foo')

        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(function='foo')

        ex = cm.exception
        self.assertEqual(str(ex), 'Required argument missing for foo')

        with self.assertRaises(RequiredArgument) as cm:
            raise RequiredArgument(argument='foo', function='bar')

        ex = cm.exception
        self.assertEqual(str(ex), 'bar requires a foo argument')

    def test_is_gvm_error(self):
        with self.assertRaises(GvmError):
            raise RequiredArgument('foo bar')


class GvmServerErrorTestCase(unittest.TestCase):
    def test_raise_with_message_and_status(self):
        with self.assertRaisesRegex(GvmServerError, '^Server Error foo. bar$'):
            raise GvmServerError('foo', 'bar')

    def test_is_gvm_error(self):
        with self.assertRaises(GvmError):
            raise GvmServerError('foo', 'bar')


class GvmResponseErrorTestCase(unittest.TestCase):
    def test_raise_with_message_and_status(self):
        with self.assertRaisesRegex(
            GvmResponseError, '^Response Error foo. bar$'
        ):
            raise GvmResponseError('foo', 'bar')

    def test_is_gvm_error(self):
        with self.assertRaises(GvmError):
            raise GvmResponseError('foo', 'bar')


class InvalidArgumentTypeTestCase(unittest.TestCase):
    def test_raise_with_argument_and_arg_type(self):
        with self.assertRaisesRegex(
            InvalidArgumentType, '^The argument foo must be of type bar.$'
        ):
            raise InvalidArgumentType('foo', 'bar')

    def test_raise_with_function(self):
        with self.assertRaisesRegex(
            InvalidArgumentType,
            '^In baz the argument foo must be of type bar.$',
        ):
            raise InvalidArgumentType('foo', 'bar', function='baz')

    def test_string_conversion(self):
        with self.assertRaises(InvalidArgumentType) as cm:
            raise InvalidArgumentType('foo', 'bar')

        ex = cm.exception
        self.assertEqual(str(ex), 'The argument foo must be of type bar.')
        self.assertIsNone(ex.function)

        with self.assertRaises(InvalidArgumentType) as cm:
            raise InvalidArgumentType('foo', 'bar', function='baz')

        ex = cm.exception
        self.assertEqual(
            str(ex), 'In baz the argument foo must be of type bar.'
        )

    def test_is_gvm_error(self):
        with self.assertRaises(GvmError):
            raise InvalidArgumentType('foo', 'bar')


if __name__ == '__main__':
    unittest.main()
