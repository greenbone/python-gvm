# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
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

from tests.protocols import GmpTestCase

from gvm.errors import GvmError

from gvm.protocols.gmp import Gmp
from gvm.protocols.gmpv7 import Gmp as Gmpv7
from gvm.protocols.gmpv8 import Gmp as Gmpv8
from gvm.protocols.gmpv9 import Gmp as Gmpv9
from gvm.protocols.gmpv208 import Gmp as Gmpv208
from gvm.protocols.gmpv214 import Gmp as Gmpv214


class GmpContextManagerTestCase(GmpTestCase):

    gmp_class = Gmp

    def test_select_gmpv7(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>7.0</version>'
            '</get_version_response>'
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (7,))
            self.assertIsInstance(gmp, Gmpv7)

    def test_select_gmpv8(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>8.0</version>'
            '</get_version_response>'
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (8,))
            self.assertIsInstance(gmp, Gmpv8)

    def test_select_gmpv9(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>9.0</version>'
            '</get_version_response>'
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (9,))
            self.assertIsInstance(gmp, Gmpv9)

    def test_select_gmpv208(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>20.08</version>'
            '</get_version_response>'
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (20, 8))
            self.assertIsInstance(gmp, Gmpv208)

    def test_select_gmpv214(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>21.04</version>'
            '</get_version_response>'
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (21, 4))
            self.assertIsInstance(gmp, Gmpv214)

    def test_unknown_protocol(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<version>1.0</version>'
            '</get_version_response>'
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_missing_version_in_response(self):
        self.connection.read.return_value(
            '<get_version_response status="200" status_text="OK">'
            '<foo>bar</foo>'
            '</get_version_response>'
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_invalid_response(self):
        self.connection.read.return_value('<get_foo_response/>')

        with self.assertRaises(GvmError):
            with self.gmp:
                pass


if __name__ == '__main__':
    unittest.main()
