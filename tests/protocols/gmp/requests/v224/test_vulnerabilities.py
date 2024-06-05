# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Vulnerabilities


class VulnerabilitiesTestCase(unittest.TestCase):
    def test_get_vulnerabilities(self):
        request = Vulnerabilities.get_vulnerabilities()
        self.assertEqual(bytes(request), b"<get_vulns/>")

    def test_get_vulnerabilities_with_filter_string(self):
        request = Vulnerabilities.get_vulnerabilities(
            filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_vulns filter="filter_string"/>',
        )

    def test_get_vulnerabilities_with_filter_id(self):
        request = Vulnerabilities.get_vulnerabilities(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_vulns filt_id="filter_id"/>',
        )

    def test_get_vulnerability(self):
        request = Vulnerabilities.get_vulnerability("vulnerability_id")
        self.assertEqual(
            bytes(request),
            b'<get_vulns vuln_id="vulnerability_id"/>',
        )

    def test_get_vulnerability_missing_vulnerability_id(self):
        with self.assertRaises(RequiredArgument):
            Vulnerabilities.get_vulnerability(None)

        with self.assertRaises(RequiredArgument):
            Vulnerabilities.get_vulnerability("")
