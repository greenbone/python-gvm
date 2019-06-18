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

from tests import CallableMock


class MockConnection:
    def __init__(self):
        self.connect = CallableMock('connect')
        self.disconnect = CallableMock('disconnect')
        self.send = CallableMock('send')
        self.read = CallableMock('read')
        self.read.return_value('<foo_response status="200"/>')
        self.finish_send = CallableMock('finish_send')


class GmpTestCase(unittest.TestCase):

    gmp_class = None

    def setUp(self):
        self.connection = MockConnection()
        # pylint: disable=not-callable
        self.gmp = self.gmp_class(self.connection)
