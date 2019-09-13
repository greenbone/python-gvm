# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import unittest

import os
import socketserver
import tempfile
import threading
import uuid

from gvm.connections import UnixSocketConnection, DEFAULT_TIMEOUT
from gvm.errors import GvmError


class DummyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = bytes(
            "<gmp_response status=\"200\" status_text=\"OK\"/>", 'utf-8'
        )
        self.request.sendall(response)


class ThreadedUnixStreamServer(
    socketserver.ThreadingMixIn, socketserver.UnixStreamServer
):
    pass


class UnixSocketConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.socketname = "%s/%s.sock" % (
            tempfile.gettempdir(),
            str(uuid.uuid4()),
        )
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
        self.connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        self.connection.connect()
        self.connection.read()
        self.connection.disconnect()

    def test_unix_socket_connection_connect_send_bytes_read(self):
        self.connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        self.connection.connect()
        self.connection.send(bytes("<gmp/>", 'utf-8'))
        self.connection.read()
        self.connection.disconnect()

    def test_unix_socket_connection_connect_send_str_read(self):
        self.connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        self.connection.connect()
        self.connection.send("<gmp/>")
        self.connection.read()
        self.connection.disconnect()

    def test_unix_socket_send_unconnected_socket(self):
        self.connection = UnixSocketConnection(
            path=self.socketname, timeout=DEFAULT_TIMEOUT
        )
        with self.assertRaises(GvmError):
            self.connection.send("<gmp>/")


if __name__ == '__main__':
    unittest.main()
