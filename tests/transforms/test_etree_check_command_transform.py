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

from gvm.errors import GvmError
from gvm.transforms import EtreeCheckCommandTransform


class EtreeCheckCommandTransformTestCase(unittest.TestCase):
    def test_no_status_transform(self):
        transform = EtreeCheckCommandTransform()

        with self.assertRaises(GvmError):
            transform('<foo/')

    def test_no_success_status_transform(self):
        transform = EtreeCheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '400')
        root.set('status_text', 'Foo error')

        response = etree.tostring(root).decode('utf-8')

        with self.assertRaises(GvmError):
            transform(response)

    def test_success_response(self):
        transform = EtreeCheckCommandTransform()

        root = etree.Element('foo_response')
        root.set('status', '200')

        response = etree.tostring(root).decode('utf-8')

        result = transform(response)

        self.assertTrue(etree.iselement(result))
        self.assertEqual(result.tag, 'foo_response')
        self.assertEqual(result.get('status'), '200')
