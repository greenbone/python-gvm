# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from unittest.mock import MagicMock

from gvm.connections import (
    DEFAULT_TIMEOUT,
    GvmConnection,
)
from gvm.connections._connection import AbstractGvmConnection
from gvm.errors import GvmError


class DummyConnection(AbstractGvmConnection):
    def connect(self) -> None:
        pass


class GvmConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access
    def test_init_no_args(self):
        connection = DummyConnection()

        self.assertIsNone(connection._socket)
        self.assertEqual(connection._timeout, DEFAULT_TIMEOUT)

    def test_init_with_none(self):
        connection = DummyConnection(timeout=None)

        self.assertIsNone(connection._socket)
        self.assertEqual(connection._timeout, DEFAULT_TIMEOUT)

    def test_read_no_data(self):
        read_mock = MagicMock()
        read_mock.return_value = None

        connection = DummyConnection()
        connection._read = read_mock

        with self.assertRaises(GvmError, msg="Remote closed the connection"):
            connection.read()

    def test_read_connection_reset(self):
        read_mock = MagicMock()
        read_mock.side_effect = ConnectionResetError("Connection reset")

        connection = DummyConnection()
        connection._read = read_mock

        with self.assertRaisesRegex(
            GvmError, "^Remote closed the connection. Error was "
        ):
            connection.read()

    def test_send_not_connected(self):
        connection = DummyConnection()

        with self.assertRaisesRegex(GvmError, "^Socket is not connected$"):
            connection.send(b"<gmp/>")

    def test_send_remote_closed(self):
        for error in (
            BrokenPipeError("Broken pipe"),
            ConnectionResetError("Connection reset"),
            ConnectionAbortedError("Connection aborted"),
        ):
            with self.subTest(error=type(error).__name__):
                connection = DummyConnection()
                connection._socket = MagicMock()
                connection._socket.sendall.side_effect = error

                with self.assertRaisesRegex(
                    GvmError, "^Remote closed the connection. Error was "
                ) as cm:
                    connection.send(b"<gmp/>")

                self.assertIs(cm.exception.__cause__, error)

    def test_send_other_os_error_is_not_wrapped(self):
        connection = DummyConnection()
        connection._socket = MagicMock()
        connection._socket.sendall.side_effect = TimeoutError("timed out")

        with self.assertRaises(TimeoutError):
            connection.send(b"<gmp/>")

    def test_read_trigger_timeout(self):
        # mocking the response into two parts, so we run into the timeout
        # check in the loop
        read_mock = MagicMock()
        read_mock.side_effect = [b"<foo>xyz<bar></bar>", b"</foo>"]

        connection = DummyConnection(timeout=0)
        connection._read = read_mock

        with self.assertRaises(
            GvmError, msg="Timeout while reading the response"
        ):
            connection.read()

    def test_is_gvm_connection(self):
        connection = DummyConnection()
        self.assertTrue(isinstance(connection, GvmConnection))
