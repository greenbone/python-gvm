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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv214 import SeverityLevel, get_severity_level_from_string


class GetSeverityLevelFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_severity_level_from_string('foo')

    def test_none_or_empty(self):
        ct = get_severity_level_from_string(None)
        self.assertIsNone(ct)
        ct = get_severity_level_from_string('')
        self.assertIsNone(ct)

    def test_high(self):
        ct = get_severity_level_from_string('High')
        self.assertEqual(ct, SeverityLevel.HIGH)

    def test_medium(self):
        ct = get_severity_level_from_string('Medium')
        self.assertEqual(ct, SeverityLevel.MEDIUM)

    def test_low(self):
        ct = get_severity_level_from_string('Low')
        self.assertEqual(ct, SeverityLevel.LOW)

    def test_log(self):
        ct = get_severity_level_from_string('Log')
        self.assertEqual(ct, SeverityLevel.LOG)

    def test_alarm(self):
        ct = get_severity_level_from_string('Alarm')
        self.assertEqual(ct, SeverityLevel.ALARM)


if __name__ == '__main__':
    unittest.main()
