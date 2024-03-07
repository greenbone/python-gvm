# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.connections import DebugConnection, GvmConnection
from gvm.connections._connection import AbstractGvmConnection


class TestConnection(AbstractGvmConnection):
    def connect(self) -> None:
        pass


class DebugConnectionTestCase(unittest.TestCase):
    def test_is_gvm_connection(self):
        connection = DebugConnection(TestConnection())
        self.assertTrue(isinstance(connection, GvmConnection))
