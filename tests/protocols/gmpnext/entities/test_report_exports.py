#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_exports import (
    GmpGetReportExportsTestMixin,
    GmpGetReportExportTestMixin,
)


class GmpGmpGetReportExportsTestCase(GmpGetReportExportsTestMixin, GMPTestCase):
    pass


class GmpGmpGetReportExportTestCase(GmpGetReportExportTestMixin, GMPTestCase):
    pass
