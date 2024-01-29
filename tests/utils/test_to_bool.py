# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.utils import to_bool


class TestToBool(unittest.TestCase):
    def test_to_bool(self):
        true = to_bool(True)
        self.assertEqual("1", true)

        false = to_bool(False)
        self.assertEqual("0", false)


if __name__ == "__main__":
    unittest.main()
