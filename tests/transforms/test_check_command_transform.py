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

from lxml import etree

from gvm.errors import GvmError, GvmResponseError, GvmServerError
from gvm.transforms import CheckCommandTransform


class CheckCommandTransformTestCase(unittest.TestCase):
    def test_no_status_transform(self):
        transform = CheckCommandTransform()

        with self.assertRaises(GvmError):
            transform('<foo/')

    def test_no_success_300status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '300')
        root.set('status_text', 'Foo error')

        response = etree.tostring(root).decode('utf-8')

        with self.assertRaises(GvmError):
            transform(response)

    def test_no_success_400status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '400')
        root.set('status_text', 'Foo error')

        response = etree.tostring(root).decode('utf-8')

        with self.assertRaises(GvmResponseError):
            transform(response)

    def test_no_success_500status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '500')
        root.set('status_text', 'Foo error')

        response = etree.tostring(root).decode('utf-8')

        with self.assertRaises(GvmServerError):
            transform(response)

    def test_success_response(self):
        transform = CheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '200')

        response = etree.tostring(root).decode('utf-8')

        self.assertEqual(transform(response), '<foo_response status="200"/>')
