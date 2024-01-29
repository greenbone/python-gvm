# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.utils import to_comma_list


class TestToCoCommaList(unittest.TestCase):
    def test_to_comma_list(self):
        # pylint: disable=invalid-name
        the_list = ["foo", "bar", "baz"]

        comma_string = to_comma_list(the_list)

        self.assertEqual("foo,bar,baz", comma_string)


if __name__ == "__main__":
    unittest.main()
