# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from lxml import etree

from gvm.errors import GvmError, GvmResponseError, GvmServerError
from gvm.transforms import CheckCommandTransform


class CheckCommandTransformTestCase(unittest.TestCase):
    def test_no_status_transform(self):
        transform = CheckCommandTransform()

        with self.assertRaises(GvmError):
            transform(b"<foo/>")

    def test_no_success_300status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "300")
        root.set("status_text", "Foo error")

        response = etree.tostring(root)

        with self.assertRaises(GvmError):
            transform(response)

    def test_no_success_400status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "400")
        root.set("status_text", "Foo error")

        response = etree.tostring(root)

        with self.assertRaises(GvmResponseError):
            transform(response)

    def test_no_success_500status_transform(self):
        transform = CheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "500")
        root.set("status_text", "Foo error")

        response = etree.tostring(root)

        with self.assertRaises(GvmServerError):
            transform(response)

    def test_success_response(self):
        transform = CheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "200")

        response = etree.tostring(root)

        self.assertEqual(transform(response), b'<foo_response status="200"/>')
