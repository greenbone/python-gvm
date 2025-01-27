# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226 import GMPTestCase
from .reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)


class GMPDeleteReportTestCase(GmpDeleteReportTestMixin, GMPTestCase):
    pass


class GMPGetReportTestCase(GmpGetReportTestMixin, GMPTestCase):
    pass


class GMPGetReportsTestCase(GmpGetReportsTestMixin, GMPTestCase):
    pass


class GMPImportReportTestCase(GmpImportReportTestMixin, GMPTestCase):
    pass
