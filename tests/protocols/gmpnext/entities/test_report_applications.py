# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_applications.test_get_report_applications import (
    GmpGetReportApplicationsTestMixin,
)


class GmpGetReportApplicationsTestCase(
    GmpGetReportApplicationsTestMixin, GMPTestCase
):
    pass
