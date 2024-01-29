# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
import warnings

from gvm.utils import deprecation


class TestDeprecation(unittest.TestCase):
    def test_deprecation(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            self.assertEqual(len(w), 0)

            warnings.simplefilter("always")

            deprecation("I am deprecated")

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn(str(w[0].message), "I am deprecated")


if __name__ == "__main__":
    unittest.main()
