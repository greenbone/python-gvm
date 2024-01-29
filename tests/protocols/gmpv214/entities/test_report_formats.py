# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetReportFormatTestCase(
    GmpGetReportFormatTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, Gmpv214TestCase
):
    pass
