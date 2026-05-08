# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_closed_cves.test_get_report_closed_cves import (
    GmpGetReportClosedCVEsTestMixin,
)


class GmpGetReportClosedCVEsTestCase(
    GmpGetReportClosedCVEsTestMixin, GMPTestCase
):
    pass
