# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226 import GMPTestCase
from .report_configs import (
    GMPCloneReportConfigTestMixin,
    GMPCreateReportConfigTestMixin,
    GMPDeleteReportConfigTestMixin,
    GMPGetReportConfigsTestMixin,
    GMPGetReportConfigTestMixin,
    GMPModifyReportConfigTestMixin,
)


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
