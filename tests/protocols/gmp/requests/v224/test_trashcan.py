# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import TrashCan


class TrashCanTestCase(unittest.TestCase):
    def test_empty_trashcan(self):
        request = TrashCan.empty_trashcan()

        self.assertEqual(bytes(request), b"<empty_trashcan/>")

    def test_restore_from_trashcan(self):
        request = TrashCan.restore_from_trashcan("1")

        self.assertEqual(bytes(request), b'<restore id="1"/>')

    def test_restore_from_trashcan_with_empty_id(self):
        with self.assertRaises(RequiredArgument):
            TrashCan.restore_from_trashcan("")
