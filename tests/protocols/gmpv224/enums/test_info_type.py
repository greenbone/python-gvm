# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv224 import InfoType


class GetInfoTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            InfoType.from_string("foo")

    def test_none_or_empty(self):
        ct = InfoType.from_string(None)
        self.assertIsNone(ct)
        ct = InfoType.from_string("")
        self.assertIsNone(ct)

    def test_cert_bund_adv(self):
        ct = InfoType.from_string("cert_bund_adv")
        self.assertEqual(ct, InfoType.CERT_BUND_ADV)

    def test_cpe(self):
        ct = InfoType.from_string("cpe")
        self.assertEqual(ct, InfoType.CPE)

    def test_cve(self):
        ct = InfoType.from_string("cve")
        self.assertEqual(ct, InfoType.CVE)

    def test_dfn_cert_adv(self):
        ct = InfoType.from_string("dfn_cert_adv")
        self.assertEqual(ct, InfoType.DFN_CERT_ADV)

    def test_nvt(self):
        ct = InfoType.from_string("nvt")
        self.assertEqual(ct, InfoType.NVT)

    def test_ovaldef(self):
        ct = InfoType.from_string("ovaldef")
        self.assertEqual(ct, InfoType.OVALDEF)

    def test_allinfo(self):
        with self.assertRaises(InvalidArgument):
            InfoType.from_string("allinfo")


if __name__ == "__main__":
    unittest.main()
