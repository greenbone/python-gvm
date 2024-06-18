# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from lxml import etree

from gvm.errors import GvmError
from gvm.transforms import EtreeCheckCommandTransform


class EtreeCheckCommandTransformTestCase(unittest.TestCase):
    def test_no_status_transform(self):
        transform = EtreeCheckCommandTransform()

        with self.assertRaises(GvmError):
            transform(b"<foo/>")

    def test_no_success_status_transform(self):
        transform = EtreeCheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "400")
        root.set("status_text", "Foo error")

        response = etree.tostring(root)

        with self.assertRaises(GvmError):
            transform(response)

    def test_success_response(self):
        transform = EtreeCheckCommandTransform()

        root = etree.Element("foo_response")
        root.set("status", "200")

        response = etree.tostring(root)

        result = transform(response)

        self.assertTrue(etree.iselement(result))
        self.assertEqual(result.tag, "foo_response")
        self.assertEqual(result.get("status"), "200")
