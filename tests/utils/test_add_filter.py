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

from gvm.utils import add_filter
from gvm.xml import XmlCommand


class TestAddFilter(unittest.TestCase):
    def test_add_filter(self):
        cmd = XmlCommand("test")
        filter_string = "foo"

        add_filter(cmd, filter_string=filter_string, filter_id=None)

        self.assertEqual(cmd.to_string(), '<test filter="foo"/>')

    def test_add_filter_id(self):
        cmd = XmlCommand("test")
        filter_id = "foo"

        add_filter(cmd, filter_string=None, filter_id=filter_id)

        self.assertEqual(cmd.to_string(), '<test filt_id="foo"/>')


if __name__ == "__main__":
    unittest.main()
