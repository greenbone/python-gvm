# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv214 import SeverityLevel


class GetSeverityLevelFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            SeverityLevel.from_string("foo")

    def test_none_or_empty(self):
        ct = SeverityLevel.from_string(None)
        self.assertIsNone(ct)
        ct = SeverityLevel.from_string("")
        self.assertIsNone(ct)

    def test_high(self):
        ct = SeverityLevel.from_string("High")
        self.assertEqual(ct, SeverityLevel.HIGH)

    def test_medium(self):
        ct = SeverityLevel.from_string("Medium")
        self.assertEqual(ct, SeverityLevel.MEDIUM)

    def test_low(self):
        ct = SeverityLevel.from_string("Low")
        self.assertEqual(ct, SeverityLevel.LOW)

    def test_log(self):
        ct = SeverityLevel.from_string("Log")
        self.assertEqual(ct, SeverityLevel.LOG)

    def test_alarm(self):
        ct = SeverityLevel.from_string("Alarm")
        self.assertEqual(ct, SeverityLevel.ALARM)


if __name__ == "__main__":
    unittest.main()
