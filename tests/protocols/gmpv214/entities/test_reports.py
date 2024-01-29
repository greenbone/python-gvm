# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteReportTestCase(GmpDeleteReportTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetReportTestCase(GmpGetReportTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetReportsTestCase(GmpGetReportsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ImportReportTestCase(GmpImportReportTestMixin, Gmpv214TestCase):
    pass
