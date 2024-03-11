# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.protocols.core import Response, StatusError
from gvm.xml import Element, XmlError


class RequestMock:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __bytes__(self) -> bytes:
        return self._data


class ResponseTestCase(unittest.TestCase):

    def test_data(self) -> None:
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)

        self.assertEqual(response.data, b"<response/>")

    def test_bytes(self) -> None:
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)

        self.assertEqual(bytes(response), b"<response/>")

    def test_request(self) -> None:
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)

        self.assertEqual(response.request, request)

    def test_status_code(self):
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)
        self.assertIsNone(response.status_code)

        response = Response(data=b'<response status="abc"/>', request=request)
        self.assertIsNone(response.status_code)

        response = Response(data=b'<response status="123"/>', request=request)
        self.assertEqual(response.status_code, 123)

    def test_is_success(self):
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)
        self.assertFalse(response.is_success)

        response = Response(data=b'<response status="abc"/>', request=request)
        self.assertFalse(response.is_success)

        response = Response(data=b'<response status="123"/>', request=request)
        self.assertFalse(response.is_success)

        response = Response(data=b'<response status="234"/>', request=request)
        self.assertTrue(response.is_success)

    def test_raise_for_status(self):
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response/>", request=request)

        with self.assertRaisesRegex(StatusError, "^Invalid status code None$"):
            response.raise_for_status()

        response = Response(data=b'<response status="abc"/>', request=request)
        with self.assertRaisesRegex(StatusError, "^Invalid status code None$"):
            response.raise_for_status()

        response = Response(data=b'<response status="123"/>', request=request)
        with self.assertRaisesRegex(StatusError, "^Invalid status code 123$"):
            response.raise_for_status()

        response = Response(data=b'<response status="234"/>', request=request)
        self.assertIs(response.raise_for_status(), response)

    def test_xml(self):
        request = RequestMock(b"<request/>")
        response = Response(
            data=b'<response><some data="lorem"/></response>', request=request
        )

        xml = response.xml()
        self.assertIsInstance(xml, Element)

        self.assertEqual(xml.tag, "response")
        sub_element = xml[0]
        self.assertEqual(sub_element.tag, "some")
        self.assertEqual(sub_element.attrib["data"], "lorem")

    def test_invalid_xml(self):
        request = RequestMock(b"<request/>")
        response = Response(data=b"<response</response>", request=request)

        with self.assertRaisesRegex(
            XmlError, "^Invalid XML b'<response</response>'. Error was .*$"
        ):
            response.xml()
