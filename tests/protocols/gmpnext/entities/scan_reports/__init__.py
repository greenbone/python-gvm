#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_export_delta_scan_report import (
    GmpExportDeltaScanReportTestMixin,
)
from .test_export_scan_report import (
    GmpExportScanReportTestMixin,
)
from .test_get_scan_report import (
    GmpGetScanReportTestMixin,
)

__all__ = (
    "GmpExportDeltaScanReportTestMixin",
    "GmpExportScanReportTestMixin",
    "GmpGetScanReportTestMixin",
)
