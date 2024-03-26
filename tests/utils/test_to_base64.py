# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.utils import to_base64


class TestToBase64(unittest.TestCase):
    def test_to_base64(self):
        foo64 = to_base64("foo")
        self.assertEqual("Zm9v", foo64)

        bar64 = to_base64("bar")
        self.assertEqual("YmFy", bar64)


if __name__ == "__main__":
    unittest.main()
