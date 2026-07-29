# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from ...gmpnext.entities.audit_report import (
    GmpGetAuditReportLegacyTestMixin,
    GmpGetAuditReportTestMixin,
)


class GmpGetAuditReportTestCase(GmpGetAuditReportTestMixin, GMPTestCase):
    pass


class GmpGetAuditReportLegacyTestCase(
    GmpGetAuditReportLegacyTestMixin, GMPTestCase
):
    pass
