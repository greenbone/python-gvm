# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.http.core.headers import ContentType


class ContentTypeTestCase(unittest.TestCase):

    def test_from_empty_string(self):
        ct = ContentType.from_string("")
        self.assertEqual("application/octet-stream", ct.media_type)
        self.assertEqual({}, ct.params)
        self.assertEqual(None, ct.charset)

    def test_from_basic_string(self):
        ct = ContentType.from_string("text/html")
        self.assertEqual("text/html", ct.media_type)
        self.assertEqual({}, ct.params)
        self.assertEqual(None, ct.charset)

    def test_from_string_with_charset(self):
        ct = ContentType.from_string("text/html; charset=utf-32 ")
        self.assertEqual("text/html", ct.media_type)
        self.assertEqual({"charset": "utf-32"}, ct.params)
        self.assertEqual("utf-32", ct.charset)

    def test_from_string_with_param(self):
        ct = ContentType.from_string("multipart/form-data; boundary===boundary==; charset=utf-32 ")
        self.assertEqual("multipart/form-data", ct.media_type)
        self.assertEqual({"boundary": "==boundary==", "charset": "utf-32"}, ct.params)
        self.assertEqual("utf-32", ct.charset)

    def test_from_string_with_valueless_param(self):
        ct = ContentType.from_string("text/html; x-foo")
        self.assertEqual("text/html", ct.media_type)
        self.assertEqual({"x-foo": True}, ct.params)
        self.assertEqual(None, ct.charset)
