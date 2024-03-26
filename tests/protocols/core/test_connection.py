# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import GvmError
from gvm.protocols.core import Connection, InvalidStateError


class RequestMock:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __bytes__(self) -> bytes:
        return self._data


class ConnectionTestCase(unittest.TestCase):
    def test_send_request(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")

    def test_receive_data(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        connection.send(request)
        response = connection.receive_data(b"<response")

        self.assertIsNone(response)
        response = connection.receive_data(b' status="200"/>')

        self.assertIsNotNone(response)
        self.assertTrue(response.is_success)  # type: ignore

        another_request = RequestMock(b"<another_request/>")
        connection.send(another_request)

        response = connection.receive_data(b"<another_response")

        self.assertIsNone(response)
        response = connection.receive_data(b' status="200"/>')

        self.assertIsNotNone(response)
        self.assertTrue(response.is_success)  # type: ignore

    def test_receive_invalid_data(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        connection.send(request)
        with self.assertRaisesRegex(
            GvmError,
            "^Cannot parse XML response. Response data read b'<response<>'$",
        ):
            connection.receive_data(b"<response<>")

    def test_error_state_close(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        connection.send(request)
        with self.assertRaisesRegex(
            GvmError,
            "^Cannot parse XML response. Response data read b'<response<>'$",
        ):
            connection.receive_data(b"<response<>")

        with self.assertRaisesRegex(
            InvalidStateError,
            "^The connection is in an error state. Please close the connection.$",
        ):
            connection.receive_data(b"<response/>")

        with self.assertRaisesRegex(
            InvalidStateError,
            "^The connection is in an error state. Please close the connection.$",
        ):
            connection.send(request)

        connection.close()
        connection.send(request)

    def test_send_when_receiving_data(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        connection.send(request)
        connection.receive_data(b"<response")

        with self.assertRaisesRegex(
            InvalidStateError,
            "^Invalid State$",
        ):
            connection.send(request)

    def test_close_before_send(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        connection.close()

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")

    def test_close_after_send(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")

        connection.close()

        with self.assertRaisesRegex(
            InvalidStateError,
            "^Invalid State$",
        ):
            connection.receive_data(b"<response")

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")

    def test_close_after_receive_data(self) -> None:
        request = RequestMock(b"<request/>")
        connection = Connection()

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")

        connection.receive_data(b"<response")

        connection.close()

        with self.assertRaisesRegex(
            InvalidStateError,
            "^Invalid State$",
        ):
            connection.receive_data(b' status="200"/>')

        data = connection.send(request)
        self.assertEqual(data, b"<request/>")
