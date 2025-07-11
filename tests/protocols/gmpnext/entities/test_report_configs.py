# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226.entities.report_configs import (
    GMPCloneReportConfigTestMixin,
    GMPCreateReportConfigTestMixin,
    GMPDeleteReportConfigTestMixin,
    GMPGetReportConfigsTestMixin,
    GMPGetReportConfigTestMixin,
    GMPModifyReportConfigTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPCloneReportConfigTestCase(GMPCloneReportConfigTestMixin, GMPTestCase):
    pass


class GMPCreateReportConfigTestCase(
    GMPCreateReportConfigTestMixin, GMPTestCase
):
    pass


class GMPDeleteReportConfigTestCase(
    GMPDeleteReportConfigTestMixin, GMPTestCase
):
    pass


class GMPGetReportConfigTestCase(GMPGetReportConfigTestMixin, GMPTestCase):
    pass


class GMPGetReportConfigsTestCase(GMPGetReportConfigsTestMixin, GMPTestCase):
    pass


class GMPModifyReportConfigTestCase(
    GMPModifyReportConfigTestMixin, GMPTestCase
):
    pass
