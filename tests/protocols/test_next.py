# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# pylint: disable=no-member

import unittest

from gvm.protocols.next import Gmp, Osp


class LatestProtocolsTestCase(unittest.TestCase):
    def test_gmp_version(self):
        self.assertEqual(Gmp.get_protocol_version(), (22, 7))

    def test_osp_version(self):
        self.assertEqual(Osp.get_protocol_version(), (1, 2))


if __name__ == "__main__":
    unittest.main()
