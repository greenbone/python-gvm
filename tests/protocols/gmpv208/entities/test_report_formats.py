# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .report_formats import (
    GmpCloneReportFormatTestMixin,
    GmpDeleteReportFormatTestMixin,
    GmpGetReportFormatsTestMixin,
    GmpGetReportFormatTestMixin,
    GmpImportReportFormatTestMixin,
    GmpModifyReportFormatTestMixin,
    GmpVerifyReportFormatTestMixin,
)


class Gmpv208DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetReportFormatTestCase(
    GmpGetReportFormatTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, Gmpv208TestCase
):
    pass
