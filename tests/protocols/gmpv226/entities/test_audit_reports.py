# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226 import GMPTestCase
from .audit_reports import (
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
