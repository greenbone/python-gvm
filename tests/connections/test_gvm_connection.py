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


class TestConnection(AbstractGvmConnection):
    def connect(self) -> None:
        pass


class GvmConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access
    def test_init_no_args(self):
        connection = TestConnection()

        self.assertIsNone(connection._socket)
        self.assertEqual(connection._timeout, DEFAULT_TIMEOUT)

    def test_init_with_none(self):
        connection = TestConnection(timeout=None)

        self.assertIsNone(connection._socket)
        self.assertEqual(connection._timeout, DEFAULT_TIMEOUT)

    def test_read_no_data(self):
        read_mock = MagicMock()
        read_mock.return_value = None

        connection = TestConnection()
        connection._read = read_mock

        with self.assertRaises(GvmError, msg="Remote closed the connection"):
            connection.read()

    def test_read_trigger_timeout(self):
        # mocking the response into two parts, so we run into the timeout
        # check in the loop
        read_mock = MagicMock()
        read_mock.side_effect = [b"<foo>xyz<bar></bar>", b"</foo>"]

        connection = TestConnection(timeout=0)
        connection._read = read_mock

        with self.assertRaises(
            GvmError, msg="Timeout while reading the response"
        ):
            connection.read()

    def test_is_gvm_connection(self):
        connection = TestConnection()
        self.assertTrue(isinstance(connection, GvmConnection))
