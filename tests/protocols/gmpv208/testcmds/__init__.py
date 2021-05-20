# -*- coding utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier GPL-3.0-or-later
#
# This program is free software you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http//www.gnu.org/licenses/>.

# pylint: disable=no-member

from .test_get_vulnerabilities import GmpGetVulnerabilitiesTestCase
from .test_get_vulnerability import GmpGetVulnerabilityTestCase
from .test_protocol_version import GmpProtocolVersionTestCase
from .test_authenticate import GmpAuthenticateTestCase
from .test_describe_auth import GmpDescribeAuthCommandTestCase
from .test_empty_trashcan import GmpEmptyTrashcanCommandTestCase
from .test_get_preference import GmpGetPreferenceTestCase
from .test_get_preferences import GmpGetPreferencesTestCase
from .test_get_setting import GmpGetSettingTestCase
from .test_get_settings import GmpGetSettingsTestCase
from .test_get_system_reports import GmpGetSystemReportsTestCase
from .test_get_version import GmpGetVersionCommandTestCase
from .test_help import GmpHelpTestCase
from .test_modify_auth import GmpModifyAuthTestCase
from .test_modify_setting import GmpModifySettingTestCase
from .test_restore import GmpRestoreTestCase
from .test_sync_cert import GmpSyncCertCommandTestCase
from .test_sync_scap import GmpSyncScapCommandTestCase
from .test_with_statement import GmpWithStatementTestCase
