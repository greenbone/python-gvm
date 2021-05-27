# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
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
from unittest.mock import patch, Mock
from gvm.connections import (
    SSHConnection,
    DEFAULT_SSH_PORT,
    DEFAULT_SSH_USERNAME,
    DEFAULT_SSH_PASSWORD,
    DEFAULT_HOSTNAME,
)
from gvm.errors import GvmError


class SSHConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access, invalid-name
    def test_init_no_args(self):
        ssh_connection = SSHConnection()

        self.check_ssh_connection_for_default_values(ssh_connection)

    def test_init_with_none(self):
        ssh_connection = SSHConnection(
            timeout=None, hostname=None, port=None, username=None, password=None
        )

        self.check_ssh_connection_for_default_values(ssh_connection)

    def check_ssh_connection_for_default_values(self, ssh_connection):
        self.assertIsInstance(ssh_connection, SSHConnection)
        self.assertEqual(ssh_connection.hostname, DEFAULT_HOSTNAME)
        self.assertEqual(ssh_connection.port, DEFAULT_SSH_PORT)
        self.assertEqual(ssh_connection.username, DEFAULT_SSH_USERNAME)
        self.assertEqual(ssh_connection.password, DEFAULT_SSH_PASSWORD)

    def test_connect_error(self):
        ssh_connection = SSHConnection()
        with self.assertRaises(GvmError, msg="SSH Connection failed"):
            ssh_connection.connect()

    def test_connect(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ['a', 'b', 'c']
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            self.assertEqual(ssh_connection._stdin, 'a')
            self.assertEqual(ssh_connection._stdout, 'b')
            self.assertEqual(ssh_connection._stderr, 'c')

    def test_disconnect(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ['a', 'b', 'c']
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            self.assertEqual(ssh_connection._stdin, 'a')
            self.assertEqual(ssh_connection._stdout, 'b')
            self.assertEqual(ssh_connection._stderr, 'c')

            ssh_connection.disconnect()
            # make sure the attributes have been deleted
            with self.assertRaises(AttributeError):
                type(ssh_connection._stdin)
            with self.assertRaises(AttributeError):
                type(ssh_connection._stdout)
            with self.assertRaises(AttributeError):
                type(ssh_connection._stderr)
            with self.assertRaises(AttributeError):
                type(ssh_connection._socket)

            with self.assertRaises(AttributeError):
                with self.assertLogs('foo', level='INFO') as cm:
                    # disconnect twice should not work ...
                    ssh_connection.disconnect()
                    self.assertEqual(
                        cm.output,
                        [
                            'Connection might already be'
                            ' closed. No socket found.',
                        ],
                    )

            ssh_connection._socket = None
            ssh_connection.disconnect()

    def test_disconnect_os_error(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ['a', 'b', 'c']
            client_mock.close.side_effect = OSError

            ssh_connection = SSHConnection()
            ssh_connection.connect()

            with self.assertRaises(OSError):
                with self.assertLogs('foo', level='INFO') as cm:
                    ssh_connection.disconnect()
                    self.assertEqual(cm.output, ['Connection closing error: '])

    def test_send(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.return_value = 4
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            req = ssh_connection.send("blah")
            self.assertEqual(req, 4)

    def test_send_error(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.return_value = None
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            with self.assertRaises(
                GvmError, msg='Remote closed the connection'
            ):
                ssh_connection.send("blah")

    def test_send_and_slice(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.side_effect = [2, 2]
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            req = ssh_connection.send("blah")
            self.assertEqual(req, 4)

            stdin.channel.send.assert_called()
            with self.assertRaises(AssertionError):
                stdin.channel.send.assert_called_once()

    def test_read(self):
        with patch('paramiko.SSHClient') as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdout = Mock()
            stdout.channel.recv.return_value = b"foo bar baz"
            client_mock.exec_command.return_value = [None, stdout, None]
            ssh_connection = SSHConnection()

            ssh_connection.connect()
            recved = ssh_connection._read()
            self.assertEqual(recved, b'foo bar baz')
