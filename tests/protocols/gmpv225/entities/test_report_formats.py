# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.report_formats import (
    GmpCloneReportFormatTestMixin,
    GmpDeleteReportFormatTestMixin,
    GmpGetReportFormatsTestMixin,
    GmpGetReportFormatTestMixin,
    GmpImportReportFormatTestMixin,
    GmpModifyReportFormatTestMixin,
    GmpVerifyReportFormatTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetReportFormatTestCase(
    GmpGetReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, Gmpv225TestCase
):
    pass
