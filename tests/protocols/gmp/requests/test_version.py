# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import Version


class VersionTestCase(unittest.TestCase):
    def test_version(self) -> None:
        request = Version.get_version()

        self.assertIsInstance(request, Request)
        self.assertEqual(bytes(request), b"<get_version/>")
