# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPGetVtsTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_get_vts_with_vt(self):
        self.osp.get_vts(vt_id="1.1.1.1.1.1")

        self.connection.send.has_been_called_with(
            b'<get_vts vt_id="1.1.1.1.1.1"/>'
        )

    def test_get_vts(self):
        self.osp.get_vts()

        self.connection.send.has_been_called_with(b"<get_vts/>")


if __name__ == "__main__":
    unittest.main()
