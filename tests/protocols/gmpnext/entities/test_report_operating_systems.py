# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_operating_systems.test_get_report_operating_systems import (
    GmpGetReportOperatingSystemsTestMixin,
)


class GmpGetReportOperatingSystemsTestCase(
    GmpGetReportOperatingSystemsTestMixin, GMPTestCase
):
    pass
