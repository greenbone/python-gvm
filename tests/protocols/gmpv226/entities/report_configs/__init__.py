# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_report_config import GMPCloneReportConfigTestMixin
from .test_create_report_config import GMPCreateReportConfigTestMixin
from .test_delete_report_config import GMPDeleteReportConfigTestMixin
from .test_get_report_config import GMPGetReportConfigTestMixin
from .test_get_report_configs import GMPGetReportConfigsTestMixin
from .test_modify_report_config import GMPModifyReportConfigTestMixin

__all__ = (
    "GMPCloneReportConfigTestMixin",
    "GMPCreateReportConfigTestMixin",
    "GMPDeleteReportConfigTestMixin",
    "GMPGetReportConfigTestMixin",
    "GMPGetReportConfigsTestMixin",
    "GMPModifyReportConfigTestMixin",
)
