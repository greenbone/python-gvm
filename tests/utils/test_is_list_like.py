# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.utils import is_list_like


class TestIsListLike(unittest.TestCase):
    def test_is_list_like(self):
        self.assertFalse(is_list_like(True))

        self.assertFalse(is_list_like("foo"))

        self.assertFalse(is_list_like(13))

        self.assertTrue(is_list_like([1]))

        self.assertTrue(is_list_like(["1", "2"]))

        self.assertTrue(is_list_like(("2", "3")))


if __name__ == "__main__":
    unittest.main()
