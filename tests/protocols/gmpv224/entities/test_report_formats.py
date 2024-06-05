# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .report_formats import (
    GmpCloneReportFormatTestMixin,
    GmpDeleteReportFormatTestMixin,
    GmpGetReportFormatsTestMixin,
    GmpGetReportFormatTestMixin,
    GmpImportReportFormatTestMixin,
    GmpModifyReportFormatTestMixin,
    GmpVerifyReportFormatTestMixin,
)


class Gmpv224DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetReportFormatTestCase(
    GmpGetReportFormatTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, Gmpv224TestCase
):
    pass
