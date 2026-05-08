# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_errors.test_get_report_errors import (
    GmpGetReportErrorsTestMixin,
)


class GmpGetReportErrorsTestCase(GmpGetReportErrorsTestMixin, GMPTestCase):
    pass
