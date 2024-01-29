# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
