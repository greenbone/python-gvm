# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.report_formats import (
    GmpCloneReportFormatTestMixin,
    GmpDeleteReportFormatTestMixin,
    GmpGetReportFormatsTestMixin,
    GmpGetReportFormatTestMixin,
    GmpImportReportFormatTestMixin,
    GmpModifyReportFormatTestMixin,
    GmpVerifyReportFormatTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, GMPTestCase
):
    pass


class Gmpv225GetReportFormatTestCase(GmpGetReportFormatTestMixin, GMPTestCase):
    pass


class Gmpv225GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, GMPTestCase
):
    pass


class Gmpv225CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, GMPTestCase
):
    pass


class Gmpv225ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, GMPTestCase
):
    pass


class Gmpv225VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, GMPTestCase
):
    pass
