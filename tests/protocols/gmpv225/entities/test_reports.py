# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteReportTestCase(GmpDeleteReportTestMixin, GMPTestCase):
    pass


class Gmpv225GetReportTestCase(GmpGetReportTestMixin, GMPTestCase):
    pass


class Gmpv225GetReportsTestCase(GmpGetReportsTestMixin, GMPTestCase):
    pass


class Gmpv225ImportReportTestCase(GmpImportReportTestMixin, GMPTestCase):
    pass
