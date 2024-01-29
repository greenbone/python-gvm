# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from unittest.mock import patch

from gvm.connections import (
    DEFAULT_TIMEOUT,
    AbstractGvmConnection,
    DebugConnection,
    GvmConnection,
    XmlReader,
)
from gvm.errors import GvmError


class XmlReaderTestCase(unittest.TestCase):
    def test_is_end_xml_false(self):
        reader = XmlReader()
        reader.start_xml()

        false = reader.is_end_xml()
        self.assertFalse(false)


class TestConnection(AbstractGvmConnection):
    def connect(self) -> None:
        pass


class GvmConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access
    def test_init_no_args(self):
        connection = TestConnection()
        self.check_for_default_values(connection)

    def test_init_with_none(self):
        connection = TestConnection(timeout=None)
        self.check_for_default_values(connection)

    def check_for_default_values(self, gvm_connection: GvmConnection):
        self.assertIsNone(gvm_connection._socket)
        self.assertEqual(gvm_connection._timeout, DEFAULT_TIMEOUT)

    @patch("gvm.connections.AbstractGvmConnection._read")
    def test_read_no_data(self, _read_mock):
        _read_mock.return_value = None
        connection = TestConnection()
        with self.assertRaises(GvmError, msg="Remote closed the connection"):
            connection.read()

    @patch("gvm.connections.AbstractGvmConnection._read")
    def test_read_trigger_timeout(self, _read_mock):
        # mocking the response into two parts, so we run into the timeout
        # check in the loop
        _read_mock.side_effect = [b"<foo>xyz<bar></bar>", b"</foo>"]
        connection = TestConnection(timeout=0)
        with self.assertRaises(
            GvmError, msg="Timeout while reading the response"
        ):
            connection.read()

    def test_is_gvm_connection(self):
        connection = TestConnection()
        self.assertTrue(isinstance(connection, GvmConnection))


class DebugConnectionTestCase(unittest.TestCase):
    def test_is_gvm_connection(self):
        connection = DebugConnection(TestConnection())
        self.assertTrue(isinstance(connection, GvmConnection))
