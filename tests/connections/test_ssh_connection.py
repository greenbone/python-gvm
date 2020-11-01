# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from gvm.connections import (
    SSHConnection,
    DEFAULT_SSH_PORT,
    DEFAULT_SSH_USERNAME,
    DEFAULT_SSH_PASSWORD,
    DEFAULT_HOSTNAME,
)


class SSHConnectionTestCase(unittest.TestCase):
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
