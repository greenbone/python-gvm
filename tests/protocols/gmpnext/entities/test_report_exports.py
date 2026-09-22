#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_exports import (
    GmpCancelReportExportTestMixin,
    GmpDownloadReportExportTestMixin,
    GmpGetReportExportsTestMixin,
    GmpGetReportExportTestMixin,
)


class GmpGmpGetReportExportsTestCase(GmpGetReportExportsTestMixin, GMPTestCase):
    pass


class GmpGmpGetReportExportTestCase(GmpGetReportExportTestMixin, GMPTestCase):
    pass


class GmpGmpDownloadReportExportTestCase(
    GmpDownloadReportExportTestMixin, GMPTestCase
):
    pass


class GmpCancelReportExportTestCase(
    GmpCancelReportExportTestMixin, GMPTestCase
):
    pass
