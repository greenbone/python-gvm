# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .audit_report.test_get_audit_report import (
    GmpGetAuditReportTestMixin,
)


class GmpGetAuditReportTestCase(GmpGetAuditReportTestMixin, GMPTestCase):
    pass
