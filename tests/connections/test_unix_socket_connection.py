# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import socketserver
import tempfile
import threading
import unittest
import uuid
from unittest.mock import patch

from gvm.connections import (
    DEFAULT_TIMEOUT,
    DEFAULT_UNIX_SOCKET_PATH,
    UnixSocketConnection,
)
from gvm.errors import GvmError


class DummyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = bytes(
            '<gmp_response status="200" status_text="OK"/>', "utf-8"
        )
        self.request.sendall(response)


class ThreadedUnixStreamServer(
    socketserver.ThreadingMixIn, socketserver.UnixStreamServer
):
    pass


class UnixSocketConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access, invalid-name
    def setUp(self):
        self.socketname = f"{tempfile.gettempdir()}/{str(uuid.uuid4())}.sock"
        self.sockserv = ThreadedUnixStreamServer(
            self.socketname, DummyRequestHandler
        )
        self.server_thread = threading.Thread(
            target=self.sockserv.serve_forever
        )
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.sockserv.shutdown()
        self.sockserv.server_close()
        os.unlink(self.socketname)

    def test_unix_socket_connection_connect_read(self):
        connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        connection.connect()
        resp = connection.read()
        self.assertEqual(resp, '<gmp_response status="200" status_text="OK"/>')
        connection.disconnect()

    def test_unix_socket_connection_connect_send_bytes_read(self):
        connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        connection.connect()
        req = connection.send(bytes("<gmp/>", "utf-8"))
        self.assertIsNone(req)
        resp = connection.read()
        self.assertEqual(resp, '<gmp_response status="200" status_text="OK"/>')
        connection.disconnect()

    def test_unix_socket_connection_connect_send_str_read(self):
        connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        connection.connect()
        req = connection.send("<gmp/>")
        self.assertIsNone(req)
        resp = connection.read()
        self.assertEqual(resp, '<gmp_response status="200" status_text="OK"/>')
        connection.disconnect()

    def test_unix_socket_connect_file_not_found(self):
        connection = UnixSocketConnection(path="foo", timeout=DEFAULT_TIMEOUT)
        with self.assertRaises(GvmError, msg="Socket foo does not exist"):
            connection.connect()
        connection.disconnect()

    def test_unix_socket_connect_could_not_connect(self):
        connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        with patch("socket.socket.connect") as ConnectMock:
            connect_mock = ConnectMock
            connect_mock.side_effect = ConnectionError
            with self.assertRaises(
                GvmError, msg=f"Could not connect to socket {self.socketname}"
            ):
                connection.connect()
            connection.disconnect()

    def test_unix_socket_send_unconnected_socket(self):
        connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
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


if __name__ == "__main__":
    unittest.main()
