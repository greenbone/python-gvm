# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import DfnCertAdvisories


class DfnCertAdvisoriesTestCase(unittest.TestCase):
    def test_get_dfn_cert_advisories(self):
        request = DfnCertAdvisories.get_dfn_cert_advisories()
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV"/>',
        )

    def test_get_dfn_cert_advisories_with_filter_string(self):
        request = DfnCertAdvisories.get_dfn_cert_advisories(
            filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV" filter="filter_string"/>',
        )

    def test_get_dfn_cert_advisories_with_filter_id(self):
        request = DfnCertAdvisories.get_dfn_cert_advisories(
            filter_id="filter_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV" filt_id="filter_id"/>',
        )

    def test_get_dfn_cert_advisories_with_name(self):
        request = DfnCertAdvisories.get_dfn_cert_advisories(name="name")
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV" name="name"/>',
        )

    def test_get_dfn_cert_advisories_with_details(self):
        request = DfnCertAdvisories.get_dfn_cert_advisories(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV" details="1"/>',
        )

        request = DfnCertAdvisories.get_dfn_cert_advisories(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="DFN_CERT_ADV" details="0"/>',
        )

    def test_get_dfn_cert_advisory(self):
        request = DfnCertAdvisories.get_dfn_cert_advisory("cert_id")
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="cert_id" type="DFN_CERT_ADV" details="1"/>',
        )

    def test_get_dfn_cert_advisory_missing_cert_id(self):
        with self.assertRaises(RequiredArgument):
            DfnCertAdvisories.get_dfn_cert_advisory(None)

        with self.assertRaises(RequiredArgument):
            DfnCertAdvisories.get_dfn_cert_advisory("")
