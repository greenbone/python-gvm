# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_ports.test_get_report_ports import (
    GmpGetReportPortsTestMixin,
)


class GmpGetReportPortsTestCase(GmpGetReportPortsTestMixin, GMPTestCase):
    pass
