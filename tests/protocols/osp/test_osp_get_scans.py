# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPGetScanTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_get_scans_with_params(self):
        self.osp.get_scans(scan_id="123-456", details=False, pop_results=False)

        self.connection.send.has_been_called_with(
            b'<get_scans scan_id="123-456" details="0" pop_results="0"/>'
        )

    def test_get_scans_default_params(self):
        self.osp.get_scans()

        self.connection.send.has_been_called_with(
            b'<get_scans details="1" pop_results="0"/>'
        )


if __name__ == "__main__":
    unittest.main()
