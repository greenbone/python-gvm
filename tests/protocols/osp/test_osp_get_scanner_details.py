# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPGetScannerDetailsTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_get_scanner_details_with_params(self):
        self.osp.get_scanner_details()

        self.connection.send.has_been_called_with(b"<get_scanner_details/>")


if __name__ == "__main__":
    unittest.main()
