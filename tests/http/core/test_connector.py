# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import unittest
from http import HTTPStatus
from typing import Any, Optional, Union
from unittest.mock import MagicMock, Mock, patch

import httpx
from httpx import HTTPError

from gvm.http.core.connector import HttpApiConnector
from gvm.http.core.headers import ContentType

TEST_JSON_HEADERS = {
    "content-type": "application/json;charset=utf-8",
    "x-example": "some-test-header",
}

JSON_EXTRA_HEADERS = {"content-length": "26"}

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


def new_mock_empty_response_func(
    method: str,
    status: Optional[Union[int, HTTPStatus]] = None,
) -> httpx.Response:
    def response_func(request_url, *_args, **_kwargs):
        response = httpx.Response(
            request=httpx.Request(method, request_url),
            content=b"",
            status_code=(
                int(HTTPStatus.NO_CONTENT) if status is None else int(status)
            ),
        )
        return response

    return response_func


def new_mock_json_response_func(
    method: str,
    content: Optional[Any] = None,
    status: Optional[Union[int, HTTPStatus]] = None,
) -> httpx.Response:
    def response_func(request_url, *_args, **_kwargs):
        response = httpx.Response(
            request=httpx.Request(method, request_url),
            content=json.dumps(content).encode(),
            status_code=int(HTTPStatus.OK) if status is None else int(status),
            headers=TEST_JSON_HEADERS,
        )
        return response

    return response_func


def new_mock_client(*, headers: Optional[dict] = None) -> Mock:
    mock = Mock(spec=httpx.Client)
    mock.headers = headers if headers is not None else {}
    return mock


class HttpApiConnectorTestCase(unittest.TestCase):
    # pylint: disable=protected-access
    def assertHasHeaders(self, expected_headers, actual_headers):
        self.assertEqual(
            expected_headers | dict(actual_headers), actual_headers
        )

    def test_url_join(self):
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "bar/baz"),
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo/", "bar/baz"),
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "./bar/baz"),
        )
        self.assertEqual(
            "http://localhost/foo/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo/", "./bar/baz"),
        )
        self.assertEqual(
            "http://localhost/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "../bar/baz"),
        )
        self.assertEqual(
            "http://localhost/bar/baz",
            HttpApiConnector.url_join("http://localhost/foo", "../bar/baz"),
        )

    def test_new_session(self):
        new_client = HttpApiConnector._new_client()
        self.assertIsInstance(new_client, httpx.Client)

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_basic_init(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        connector = HttpApiConnector("http://localhost")

        self.assertEqual("http://localhost", connector.base_url)
        new_client_mock.assert_called_once_with(None, None)
        self.assertEqual({}, mock_client.headers)

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_https_init(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        connector = HttpApiConnector(
            "https://localhost",
            server_ca_path="foo.crt",
            client_cert_paths="bar.key",
        )

        self.assertEqual("https://localhost", connector.base_url)
        new_client_mock.assert_called_once_with("foo.crt", "bar.key")
        self.assertEqual({}, mock_client.headers)

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_update_headers(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        connector = HttpApiConnector(
            "http://localhost",
        )
        connector.update_headers({"x-foo": "bar"})
        connector.update_headers({"x-baz": "123"})

        self.assertEqual({"x-foo": "bar", "x-baz": "123"}, mock_client.headers)

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_delete(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.delete.side_effect = new_mock_json_response_func(
            "DELETE", TEST_JSON_RESPONSE_BODY
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.delete(
            "foo", params={"bar": "123"}, headers={"baz": "456"}
        )

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.delete.assert_called_once_with(
            "https://localhost/foo",
            params={"bar": "123"},
            headers={"baz": "456"},
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_minimal_delete(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.delete.side_effect = new_mock_empty_response_func("DELETE")
        connector = HttpApiConnector("https://localhost")
        response = connector.delete("foo")

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_client.delete.assert_called_once_with(
            "https://localhost/foo", params=None, headers=None
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_delete_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.delete.side_effect = new_mock_empty_response_func(
            "DELETE", HTTPStatus.INTERNAL_SERVER_ERROR
        )
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(httpx.HTTPError, connector.delete, "foo")

        mock_client.delete.assert_called_once_with(
            "https://localhost/foo", params=None, headers=None
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_delete_no_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.delete.side_effect = new_mock_json_response_func(
            "DELETE",
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.delete(
            "foo",
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False,
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.delete.assert_called_once_with(
            "https://localhost/foo",
            params={"bar": "123"},
            headers={"baz": "456"},
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_get(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.get.side_effect = new_mock_json_response_func(
            "GET", TEST_JSON_RESPONSE_BODY
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.get(
            "foo", params={"bar": "123"}, headers={"baz": "456"}
        )

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.get.assert_called_once_with(
            "https://localhost/foo",
            params={"bar": "123"},
            headers={"baz": "456"},
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_minimal_get(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.get.side_effect = new_mock_empty_response_func("GET")
        connector = HttpApiConnector("https://localhost")
        response = connector.get("foo")

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_client.get.assert_called_once_with(
            "https://localhost/foo", params=None, headers=None
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_get_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.get.side_effect = new_mock_empty_response_func(
            "GET", HTTPStatus.INTERNAL_SERVER_ERROR
        )
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(HTTPError, connector.get, "foo")

        mock_client.get.assert_called_once_with(
            "https://localhost/foo", params=None, headers=None
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_get_no_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.get.side_effect = new_mock_json_response_func(
            "GET",
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.get(
            "foo",
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False,
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.get.assert_called_once_with(
            "https://localhost/foo",
            params={"bar": "123"},
            headers={"baz": "456"},
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_post_json(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.post.side_effect = new_mock_json_response_func(
            "POST", TEST_JSON_RESPONSE_BODY
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json(
            "foo",
            json={"number": 5},
            params={"bar": "123"},
            headers={"baz": "456"},
        )

        self.assertEqual(int(HTTPStatus.OK), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.post.assert_called_once_with(
            "https://localhost/foo",
            json={"number": 5},
            params={"bar": "123"},
            headers={"baz": "456"},
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_minimal_post_json(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.post.side_effect = new_mock_empty_response_func("POST")
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json("foo", TEST_JSON_REQUEST_BODY)

        self.assertEqual(int(HTTPStatus.NO_CONTENT), response.status)
        self.assertEqual(None, response.body)
        self.assertEqual(TEST_EMPTY_CONTENT_TYPE, response.content_type)
        self.assertEqual({}, response.headers)

        mock_client.post.assert_called_once_with(
            "https://localhost/foo",
            json=TEST_JSON_REQUEST_BODY,
            params=None,
            headers=None,
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_post_json_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.post.side_effect = new_mock_empty_response_func(
            "POST", HTTPStatus.INTERNAL_SERVER_ERROR
        )
        connector = HttpApiConnector("https://localhost")
        self.assertRaises(
            HTTPError, connector.post_json, "foo", json=TEST_JSON_REQUEST_BODY
        )

        mock_client.post.assert_called_once_with(
            "https://localhost/foo",
            json=TEST_JSON_REQUEST_BODY,
            params=None,
            headers=None,
        )

    @patch("gvm.http.core.connector.HttpApiConnector._new_client")
    def test_post_json_no_raise_on_status(self, new_client_mock: MagicMock):
        mock_client = new_client_mock.return_value = new_mock_client()

        mock_client.post.side_effect = new_mock_json_response_func(
            "POST",
            content=TEST_JSON_RESPONSE_BODY,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        connector = HttpApiConnector("https://localhost")
        response = connector.post_json(
            "foo",
            json=TEST_JSON_REQUEST_BODY,
            params={"bar": "123"},
            headers={"baz": "456"},
            raise_for_status=False,
        )

        self.assertEqual(int(HTTPStatus.INTERNAL_SERVER_ERROR), response.status)
        self.assertEqual(TEST_JSON_RESPONSE_BODY, response.body)
        self.assertEqual(TEST_JSON_CONTENT_TYPE, response.content_type)
        self.assertEqual(
            TEST_JSON_HEADERS | JSON_EXTRA_HEADERS, response.headers
        )

        mock_client.post.assert_called_once_with(
            "https://localhost/foo",
            json=TEST_JSON_REQUEST_BODY,
            params={"bar": "123"},
            headers={"baz": "456"},
        )
