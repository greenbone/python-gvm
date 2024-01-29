# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteReportTestCase(GmpDeleteReportTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetReportTestCase(GmpGetReportTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetReportsTestCase(GmpGetReportsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ImportReportTestCase(GmpImportReportTestMixin, Gmpv225TestCase):
    pass
