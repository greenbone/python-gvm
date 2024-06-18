# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from lxml import etree

from gvm.transforms import EtreeTransform


class EtreeTransformTestCase(unittest.TestCase):
    def test_transform_response(self):
        transform = EtreeTransform()
        result = transform(b"<foo/>")

        self.assertTrue(etree.iselement(result))

    def test_transform_more_complex_response(self):
        transform = EtreeTransform()
        result = transform(b'<foo id="bar"><lorem/><ipsum/></foo>')

        self.assertTrue(etree.iselement(result))
        self.assertEqual(result.tag, "foo")
        self.assertEqual(result.get("id"), "bar")
        self.assertEqual(len(result), 2)
