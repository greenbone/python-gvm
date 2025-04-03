# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import unittest
from http import HTTPStatus

import requests as requests_lib

from gvm.http.core.response import HttpResponse

class HttpResponseFromRequestsLibTestCase(unittest.TestCase):
    def test_from_empty_response(self):
        requests_response = requests_lib.Response()
        requests_response.status_code = int(HTTPStatus.OK)
        requests_response._content = b''

        response = HttpResponse.from_requests_lib(requests_response)

        self.assertIsNone(response.body)
        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual({}, response.headers)

    def test_from_plain_text_response(self):
        requests_response = requests_lib.Response()
        requests_response.status_code = int(HTTPStatus.OK)
        requests_response.headers.update({"content-type": "text/plain"})
        requests_response._content = b'ABCDEF'

        response = HttpResponse.from_requests_lib(requests_response)

        self.assertEqual(b'ABCDEF', response.body)
        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual({"content-type": "text/plain"}, response.headers)

    def test_from_json_response(self):
        test_content = {"foo": ["bar", 12345], "baz": True}
        requests_response = requests_lib.Response()
        requests_response.status_code = int(HTTPStatus.OK)
        requests_response.headers.update({"content-type": "application/json"})
        requests_response._content = json.dumps(test_content).encode()

        response = HttpResponse.from_requests_lib(requests_response)

        self.assertEqual(test_content, response.body)
        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual({"content-type": "application/json"}, response.headers)

    def test_from_error_json_response(self):
        test_content = {"error": "Internal server error"}
        requests_response = requests_lib.Response()
        requests_response.status_code = int(HTTPStatus.INTERNAL_SERVER_ERROR)
        requests_response.headers.update({"content-type": "application/json"})
        requests_response._content = json.dumps(test_content).encode()

        response = HttpResponse.from_requests_lib(requests_response)

        self.assertEqual(test_content, response.body)
        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual({"content-type": "application/json"}, response.headers)
