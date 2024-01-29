# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_delete_report import GmpDeleteReportTestMixin
from .test_get_report import GmpGetReportTestMixin
from .test_get_reports import GmpGetReportsTestMixin
from .test_import_report import GmpImportReportTestMixin

__all__ = (
    "GmpDeleteReportTestMixin",
    "GmpGetReportTestMixin",
    "GmpGetReportsTestMixin",
    "GmpImportReportTestMixin",
)
