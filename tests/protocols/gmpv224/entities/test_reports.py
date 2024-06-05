# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)


class Gmpv224DeleteReportTestCase(GmpDeleteReportTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetReportTestCase(GmpGetReportTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetReportsTestCase(GmpGetReportsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ImportReportTestCase(GmpImportReportTestMixin, Gmpv224TestCase):
    pass
