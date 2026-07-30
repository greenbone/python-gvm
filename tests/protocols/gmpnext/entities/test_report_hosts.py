# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_hosts.test_get_audit_report_hosts import (
    GmpGetAuditReportHostsTestMixin,
)
from .report_hosts.test_get_report_hosts import (
    GmpGetReportHostsTestMixin,
)


class GmpGetReportHostsTestCase(GmpGetReportHostsTestMixin, GMPTestCase):
    pass


class GmpGetAuditReportHostsTestCase(
    GmpGetAuditReportHostsTestMixin, GMPTestCase
):
    pass
