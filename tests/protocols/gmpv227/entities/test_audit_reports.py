# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv227 import GMPTestCase
from ...gmpv226.entities.audit_reports import (
    GmpDeleteAuditReportTestMixin,
    GmpGetAuditReportsTestMixin,
    GmpGetAuditReportTestMixin,
)


class GMPDeleteAuditReportTestCase(GmpDeleteAuditReportTestMixin, GMPTestCase):
    pass


class GMPGetAuditReportTestCase(GmpGetAuditReportTestMixin, GMPTestCase):
    pass


class GMPGetAuditReportsTestCase(GmpGetAuditReportsTestMixin, GMPTestCase):
    pass
