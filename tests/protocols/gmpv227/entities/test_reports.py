# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226.entities.reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPDeleteReportTestCase(GmpDeleteReportTestMixin, GMPTestCase):
    pass


class GMPGetReportTestCase(GmpGetReportTestMixin, GMPTestCase):
    pass


class GMPGetReportsTestCase(GmpGetReportsTestMixin, GMPTestCase):
    pass


class GMPImportReportTestCase(GmpImportReportTestMixin, GMPTestCase):
    pass
