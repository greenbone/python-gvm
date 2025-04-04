# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import unittest
from http import HTTPStatus
from typing import Optional, Any
from unittest.mock import patch, MagicMock, Mock
from requests.exceptions import HTTPError

from gvm.http.core.connector import HttpApiConnector
import requests as requests_lib

from gvm.http.core.headers import ContentType


TEST_JSON_HEADERS = {
    "content-type": "application/json;charset=utf-8",
    "x-example": "some-test-header"
}

TEST_JSON_CONTENT_TYPE = ContentType(
    media_type="application/json",
    params={"charset": "utf-8"},
    charset="utf-8",
)

TEST_EMPTY_CONTENT_TYPE = ContentType(
    media_type="application/octet-stream",
    params={},
    charset=None,
)

TEST_JSON_RESPONSE_BODY = {"response_content": True}

TEST_JSON_REQUEST_BODY = {"request_number": 5}


def new_mock_empty_response(
        status: Optional[int | HTTPStatus] = None,
) -> requests_lib.Response:
    # pylint: disable=protected-access
    response = requests_lib.Response()
    response._content = b''
    if status is None:
        response.status_code = int(HTTPStatus.NO_CONTENT)
    else:
        response.status_code = int(status)
    return response


def new_mock_json_response(
        content: Optional[Any] = None,
        status: Optional[int|HTTPStatus] = None,
)-> requests_lib.Response:
    # pylint: disable=protected-access
    response = requests_lib.Response()
    response._content = json.dumps(content).encode()

    if status is None:
        response.status_code = int(HTTPStatus.OK)
    else:
        response.status_code = int(status)

    response.headers.update(TEST_JSON_HEADERS)
    return response


def new_mock_session(
        *,
        headers: Optional[dict] = None
) -> Mock:
    mock = Mock(spec=requests_lib.Session)
    mock.headers = headers if headers is not None else {}
    return mock


class HttpApiConnectorTestCase(unittest.TestCase):
    # pylint: disable=protected-access

    def test_url_join(self):
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "bar/baz")
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo/", "bar/baz")
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "./bar/baz")
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo/", "./bar/baz")
        )
        self.assertEqual(
            "http://localhost/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "../bar/baz")
        )
        self.assertEqual(
            "http://localhost/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "../bar/baz")
        )

    def test_new_session(self):
        new_session = HttpApiConnector._new_session()
        self.assertIsInstance(new_session, requests_lib.Session)

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_basic_init(
            self,
            new_session_mock: MagicMock
    ):
        mock_session = new_session_mock.return_value = new_mock_session()

        connector = HttpApiConnector("http://localhost")

        self.assertEqual("http://localhost", connector.base_url)
        self.assertEqual(mock_session, connector._session)

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_https_init(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        connector = HttpApiConnector(
            "https://localhost",
            server_ca_path="foo.crt",
            client_cert_paths="bar.key"
        )

        self.assertEqual("https://localhost", connector.base_url)
        self.assertEqual(mock_session, connector._session)
        self.assertEqual("foo.crt", mock_session.verify)
        self.assertEqual("bar.key", mock_session.cert)

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_update_headers(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        connector = HttpApiConnector(
            "http://localhost",
        )
        connector.update_headers({"x-foo": "bar"})
        connector.update_headers({"x-baz": "123"})

        self.assertEqual({"x-foo": "bar", "x-baz": "123"}, mock_session.headers)

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_delete(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.delete.return_value = new_mock_json_response(TEST_JSON_RESPONSE_BODY)
        connector = HttpApiConnector("https://localhost")
        response = connector.delete("foo", params={"bar": "123"}, headers={"baz": "456"})

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.delete.assert_called_once_with(
            'https://localhost/foo',
            params={"bar": "123"},
            headers={"baz": "456"}
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_minimal_delete(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.delete.return_value = new_mock_empty_response()
        connector = HttpApiConnector("https://localhost")
        response = connector.delete("foo")

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_session.delete.assert_called_once_with(
            'https://localhost/foo', params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_delete_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.delete.return_value = new_mock_empty_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(
            HTTPError,
            connector.delete,
            "foo"
        )

        mock_session.delete.assert_called_once_with(
            'https://localhost/foo', params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_delete_no_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.delete.return_value = new_mock_json_response(
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.delete(
            "foo",
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.delete.assert_called_once_with(
            'https://localhost/foo',
            params={"bar": "123"},
            headers={"baz": "456"}
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_get(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.get.return_value = new_mock_json_response(TEST_JSON_RESPONSE_BODY)
        connector = HttpApiConnector("https://localhost")
        response = connector.get("foo", params={"bar": "123"}, headers={"baz": "456"})

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.get.assert_called_once_with(
            'https://localhost/foo',
            params={"bar": "123"},
            headers={"baz": "456"}
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_minimal_get(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.get.return_value = new_mock_empty_response()
        connector = HttpApiConnector("https://localhost")
        response = connector.get("foo")

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_session.get.assert_called_once_with(
            'https://localhost/foo', params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_get_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.get.return_value = new_mock_empty_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(
            HTTPError,
            connector.get,
            "foo"
        )

        mock_session.get.assert_called_once_with(
            'https://localhost/foo', params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_get_no_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.get.return_value = new_mock_json_response(
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.get(
            "foo",
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.get.assert_called_once_with(
            'https://localhost/foo',
            params={"bar": "123"},
            headers={"baz": "456"}
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_post_json(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.post.return_value = new_mock_json_response(TEST_JSON_RESPONSE_BODY)
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json(
            "foo",
            json={"number": 5},
            params={"bar": "123"},
            headers={"baz": "456"}
        )

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.post.assert_called_once_with(
            'https://localhost/foo',
            json={"number": 5},
            params={"bar": "123"},
            headers={"baz": "456"}
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_minimal_post_json(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.post.return_value = new_mock_empty_response()
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json("foo", TEST_JSON_REQUEST_BODY)

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_session.post.assert_called_once_with(
            'https://localhost/foo', json=TEST_JSON_REQUEST_BODY, params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_post_json_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.post.return_value = new_mock_empty_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(
            HTTPError,
            connector.post_json,
            "foo",
            json=TEST_JSON_REQUEST_BODY
        )

        mock_session.post.assert_called_once_with(
            'https://localhost/foo', json=TEST_JSON_REQUEST_BODY, params=None, headers=None
        )

    @patch('gvm.http.core.connector.HttpApiConnector._new_session')
    def test_post_json_no_raise_on_status(self, new_session_mock: MagicMock):
        mock_session = new_session_mock.return_value = new_mock_session()

        mock_session.post.return_value = new_mock_json_response(
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json(
            "foo",
            json=TEST_JSON_REQUEST_BODY,
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(TEST_JSON_HEADERS, response.headers)

        mock_session.post.assert_called_once_with(
            'https://localhost/foo',
            json=TEST_JSON_REQUEST_BODY,
            params={"bar": "123"},
            headers={"baz": "456"}
        )