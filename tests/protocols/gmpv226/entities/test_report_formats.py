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
from ...gmpv226 import GMPTestCase


class GMPDeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, GMPTestCase
):
    pass


class GMPGetReportFormatTestCase(GmpGetReportFormatTestMixin, GMPTestCase):
    pass


class GMPGetReportFormatsTestCase(GmpGetReportFormatsTestMixin, GMPTestCase):
    pass


class GMPCloneReportFormatTestCase(GmpCloneReportFormatTestMixin, GMPTestCase):
    pass


class GMPImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, GMPTestCase
):
    pass


class GMPModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, GMPTestCase
):
    pass


class GMPVerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, GMPTestCase
):
    pass
