# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)


class Gmpv208DeleteReportTestCase(GmpDeleteReportTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetReportTestCase(GmpGetReportTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetReportsTestCase(GmpGetReportsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ImportReportTestCase(GmpImportReportTestMixin, Gmpv208TestCase):
    pass
