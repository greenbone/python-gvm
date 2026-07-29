#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_get_audit_report import (
    GmpGetAuditReportTestMixin,
)
from .test_get_audit_report_legacy import (
    GmpGetAuditReportLegacyTestMixin,
)

__all__ = (
    "GmpGetAuditReportLegacyTestMixin",
    "GmpGetAuditReportTestMixin",
)
