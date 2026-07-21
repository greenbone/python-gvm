# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .scan_reports.test_get_scan_report import (
    GmpGetScanReportTestMixin,
)


class GmpGetScanReportTestCase(GmpGetScanReportTestMixin, GMPTestCase):
    pass
