# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from unittest.mock import Mock, patch

from gvm.connections import (
    DEFAULT_GVM_PORT,
    DEFAULT_HOSTNAME,
    DEFAULT_TIMEOUT,
    GvmConnection,
    TLSConnection,
)


class TLSConnectionTestCase(unittest.TestCase):
    def test_init_no_args(self):
        connection = TLSConnection()
        self.check_default_values(connection)

    def test_init_with_none(self):
        connection = TLSConnection(
            certfile=None,
            cafile=None,
            keyfile=None,
            hostname=None,
            port=None,
            password=None,
            timeout=None,
        )
        self.check_default_values(connection)

    def check_default_values(self, tls_connection: TLSConnection):
        self.assertIsNone(tls_connection.certfile)
        self.assertIsNone(tls_connection.cafile)
        self.assertIsNone(tls_connection.keyfile)
        self.assertEqual(tls_connection.hostname, DEFAULT_HOSTNAME)
        self.assertEqual(tls_connection.port, DEFAULT_GVM_PORT)
        self.assertIsNone(tls_connection.password)
        self.assertEqual(tls_connection._timeout, DEFAULT_TIMEOUT)

    def test_connect(self):
        with patch("ssl.SSLContext") as SSHContextMock:
            context_mock = SSHContextMock.return_value
            connection = TLSConnection()
            connection.connect()
            context_mock.wrap_socket.assert_called_once()

    def test_connect_auth(self):
        with patch("ssl.SSLContext") as SSHContextMock:
            context_mock = SSHContextMock.return_value
            cert_file = Mock()
            ca_file = Mock()
            key_file = Mock()

            connection = TLSConnection(
                certfile=cert_file, cafile=ca_file, keyfile=key_file
            )
            connection.connect()
            context_mock.load_cert_chain.assert_called_once()
            context_mock.wrap_socket.assert_called_once()
            self.assertFalse(context_mock.check_hostname)

    def test_is_gvm_connection(self):
        connection = TLSConnection()
        self.assertTrue(isinstance(connection, GvmConnection))
