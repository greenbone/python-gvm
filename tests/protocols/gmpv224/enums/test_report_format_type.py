# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import ReportFormatType


class GetPortRangeTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ReportFormatType.from_string("foo")

    def test_none_or_empty(self):
        ct = ReportFormatType.from_string(None)
        self.assertIsNone(ct)
        ct = ReportFormatType.from_string("")
        self.assertIsNone(ct)

    def test_anonymous_pdf(self):
        ct = ReportFormatType.from_string("anonymous xml")
        self.assertEqual(ct, ReportFormatType.ANONYMOUS_XML)

    def test_arf(self):
        ct = ReportFormatType.from_string("arf")
        self.assertEqual(ct, ReportFormatType.ARF)

    def test_(self):
        ct = ReportFormatType.from_string("cpe")
        self.assertEqual(ct, ReportFormatType.CPE)

    def test_csv_hosts(self):
        ct = ReportFormatType.from_string("csv hosts")
        self.assertEqual(ct, ReportFormatType.CSV_HOSTS)

    def test_csv_results(self):
        ct = ReportFormatType.from_string("csv results")
        self.assertEqual(ct, ReportFormatType.CSV_RESULTS)

    def test_gcr_pdf(self):
        ct = ReportFormatType.from_string("gcr pdf")
        self.assertEqual(ct, ReportFormatType.GCR_PDF)

    def test_gsr_html(self):
        ct = ReportFormatType.from_string("gsr html")
        self.assertEqual(ct, ReportFormatType.GSR_HTML)

    def test_gsr_pdf(self):
        ct = ReportFormatType.from_string("gsr pdf")
        self.assertEqual(ct, ReportFormatType.GSR_PDF)

    def test_gxcr_pdf(self):
        ct = ReportFormatType.from_string("gxcr pdf")
        self.assertEqual(ct, ReportFormatType.GXCR_PDF)

    def test_gxr_pdf(self):
        ct = ReportFormatType.from_string("gxr pdf")
        self.assertEqual(ct, ReportFormatType.GXR_PDF)

    def test_itg(self):
        ct = ReportFormatType.from_string("itg")
        self.assertEqual(ct, ReportFormatType.ITG)

    def test_latex(self):
        ct = ReportFormatType.from_string("latex")
        self.assertEqual(ct, ReportFormatType.LATEX)

    def test_nbe(self):
        ct = ReportFormatType.from_string("nbe")
        self.assertEqual(ct, ReportFormatType.NBE)

    def test_pdf(self):
        ct = ReportFormatType.from_string("pdf")
        self.assertEqual(ct, ReportFormatType.PDF)

    def test_svg(self):
        ct = ReportFormatType.from_string("svg")
        self.assertEqual(ct, ReportFormatType.SVG)

    def test_txt(self):
        ct = ReportFormatType.from_string("txt")
        self.assertEqual(ct, ReportFormatType.TXT)

    def test_verinice_ism(self):
        ct = ReportFormatType.from_string("verinice ism")
        self.assertEqual(ct, ReportFormatType.VERINICE_ISM)

    def test_verinice_itg(self):
        ct = ReportFormatType.from_string("verinice itg")
        self.assertEqual(ct, ReportFormatType.VERINICE_ITG)

    def test_xml(self):
        ct = ReportFormatType.from_string("xml")
        self.assertEqual(ct, ReportFormatType.XML)


if __name__ == "__main__":
    unittest.main()
