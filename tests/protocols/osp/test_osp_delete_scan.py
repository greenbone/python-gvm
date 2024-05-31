# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPDeleteScanTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_delete_scan(self):
        self.osp.delete_scan(scan_id="123-456")

        self.connection.send.has_been_called_with(
            b'<delete_scan scan_id="123-456"/>'
        )

    def test_delete_scan_without_id(self):
        with self.assertRaises(ValueError):
            self.osp.delete_scan(None)

        with self.assertRaises(ValueError):
            self.osp.delete_scan("")


if __name__ == "__main__":
    unittest.main()
