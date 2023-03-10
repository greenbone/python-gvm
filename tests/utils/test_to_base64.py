# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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

from gvm.utils import to_base64


class TestToBase64(unittest.TestCase):
    def test_to_base64(self):
        foo64 = to_base64("foo")
        self.assertEqual(b"Zm9v", foo64)

        bar64 = to_base64("bar")
        self.assertEqual(b"YmFy", bar64)


if __name__ == "__main__":
    unittest.main()
