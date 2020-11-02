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
    TLSConnection,
    DEFAULT_HOSTNAME,
    DEFAULT_GVM_PORT,
    DEFAULT_TIMEOUT,
)


class TLSConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access
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
