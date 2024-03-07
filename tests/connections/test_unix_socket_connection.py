# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import socketserver
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from gvm.connections import (
    DEFAULT_TIMEOUT,
    DEFAULT_UNIX_SOCKET_PATH,
    GvmConnection,
    UnixSocketConnection,
)
from gvm.errors import GvmError


class DummyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = b'<gmp_response status="200" status_text="OK"/>'
        self.request.sendall(response)


class ThreadedUnixStreamServer(
    socketserver.ThreadingMixIn, socketserver.UnixStreamServer
):
    pass


class UnixSocketConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access, invalid-name
    def setUp(self):
        self.socket_name = f"{tempfile.gettempdir()}/{str(uuid.uuid4())}.sock"
        self.socket_path = Path(self.socket_name)
        self.socket_server = ThreadedUnixStreamServer(
            self.socket_name, DummyRequestHandler
        )
        self.server_thread = threading.Thread(
            target=self.socket_server.serve_forever
        )
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.socket_server.server_close()
        self.socket_server.shutdown()
        self.server_thread.join(60.0)
        self.socket_path.unlink(missing_ok=True)

    def test_unix_socket_connection_connect_read(self):
        connection = UnixSocketConnection(
            path=self.socket_name, timeout=DEFAULT_TIMEOUT
        )
        connection.connect()
        resp = connection.read()
        self.assertEqual(resp, b'<gmp_response status="200" status_text="OK"/>')
        connection.disconnect()

    def test_unix_socket_connection_connect_send_bytes_read(self):
        connection = UnixSocketConnection(
            path=self.socket_name, timeout=DEFAULT_TIMEOUT
        )
        connection.connect()
        connection.send(b"<gmp/>")
        resp = connection.read()
        self.assertEqual(resp, b'<gmp_response status="200" status_text="OK"/>')
        connection.disconnect()

    def test_unix_socket_connect_file_not_found(self):
        connection = UnixSocketConnection(path="foo", timeout=DEFAULT_TIMEOUT)
        with self.assertRaises(GvmError, msg="Socket foo does not exist"):
            connection.connect()
        connection.disconnect()

    def test_unix_socket_connect_could_not_connect(self):
        connection = UnixSocketConnection(
            path=self.socket_name, timeout=DEFAULT_TIMEOUT
        )
        with patch("socket.socket.connect") as ConnectMock:
            connect_mock = ConnectMock
            connect_mock.side_effect = ConnectionError
            with self.assertRaises(
                GvmError, msg=f"Could not connect to socket {self.socket_name}"
            ):
                connection.connect()
            connection.disconnect()

    def test_unix_socket_send_unconnected_socket(self):
        connection = UnixSocketConnection(
            path=self.socket_name, timeout=DEFAULT_TIMEOUT
        )
        with self.assertRaises(GvmError, msg="Socket is not connected"):
            connection.send("<gmp>/")

    def test_init_no_args(self):
        connection = UnixSocketConnection()
        self.check_default_values(connection)

    def test_init_with_none(self):
        connection = UnixSocketConnection(path=None, timeout=None)
        self.check_default_values(connection)

    def check_default_values(self, connection: UnixSocketConnection):
        self.assertEqual(connection._timeout, DEFAULT_TIMEOUT)
        self.assertEqual(connection.path, DEFAULT_UNIX_SOCKET_PATH)

    def test_is_gvm_connection(self):
        connection = UnixSocketConnection()
        self.assertTrue(isinstance(connection, GvmConnection))
