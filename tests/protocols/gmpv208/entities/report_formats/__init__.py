# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_report_format import GmpCloneReportFormatTestMixin
from .test_delete_report_format import GmpDeleteReportFormatTestMixin
from .test_get_report_format import GmpGetReportFormatTestMixin
from .test_get_report_formats import GmpGetReportFormatsTestMixin
from .test_import_report_format import GmpImportReportFormatTestMixin
from .test_modify_report_format import GmpModifyReportFormatTestMixin
from .test_verify_report_format import GmpVerifyReportFormatTestMixin

__all__ = (
    "GmpCloneReportFormatTestMixin",
    "GmpDeleteReportFormatTestMixin",
    "GmpGetReportFormatTestMixin",
    "GmpGetReportFormatsTestMixin",
    "GmpImportReportFormatTestMixin",
    "GmpModifyReportFormatTestMixin",
    "GmpVerifyReportFormatTestMixin",
)
