# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPGetVersionTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_get_version(self):
        self.osp.get_version()

        self.connection.send.has_been_called_with("<get_version/>")


if __name__ == "__main__":
    unittest.main()
