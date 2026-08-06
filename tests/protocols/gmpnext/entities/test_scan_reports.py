# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .scan_reports import (
    GmpExportScanReportTestMixin,
    GmpGetScanReportTestMixin,
)


class GmpGetScanReportTestCase(GmpGetScanReportTestMixin, GMPTestCase):
    pass


class GmpExportScanReportTestCase(GmpExportScanReportTestMixin, GMPTestCase):
    pass
