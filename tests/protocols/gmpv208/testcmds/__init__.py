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

from .test_create_filter import GmpCreateFilterTestCase
from .test_create_permission import GmpCreatePermissionTestCase
from .test_create_tag import GmpCreateTagTestCase
from .test_get_aggregates import GmpGetAggregatesTestCase
from .test_modify_filter import GmpModifyFilterTestCase
from .test_modify_permission import GmpModifyPermissionTestCase
from .test_modify_report_format import GmpModifyReportFormatTestCase
from .test_modify_tag import GmpModifyTagTestCase
from .test_get_feed import GmpGetFeedTestCase
from .test_clone_config import GmpCloneConfigTestCase
from .test_clone_policy import GmpClonePolicyTestCase
from .test_create_config import GmpCreateConfigTestCase
from .test_create_config_from_osp_scanner import (
    GmpCreateConfigFromOSPScannerTestCase,
)
from .test_create_credential import GmpCreateCredentialTestCase
from .test_create_policy import GmpCreatePolicyTestCase
from .test_create_scanner import GmpCreateScannerTestCase
from .test_delete_config import GmpDeleteConfigTestCase
from .test_delete_policy import GmpDeletePolicyTestCase
from .test_get_config import GmpGetConfigTestCase
from .test_get_configs import GmpGetConfigsTestCase
from .test_get_policies import GmpGetPoliciesTestCase
from .test_get_policy import GmpGetPolicyTestCase
from .test_modify_credential import GmpModifyCredentialTestCase
from .test_modify_policy_set_comment import GmpModifyPolicySetCommentTestCase
from .test_modify_policy_set_family_selection import (
    GmpModifyPolicySetFamilySelectionTestCase,
)
from .test_modify_policy_set_name import GmpModifyPolicySetNameTestCase
from .test_modify_policy_set_nvt_preference import (
    GmpModifyPolicySetNvtPreferenceTestCase,
)
from .test_modify_policy_set_nvt_selection import (
    GmpModifyPolicySetNvtSelectionTestCase,
)
from .test_modify_policy_set_scanner_preference import (
    GmpModifyPolicySetScannerPreferenceTestCase,
)
from .test_modify_scanner import GmpModifyScannerTestCase
from .test_modify_ticket import GmpModifyTicketTestCase
from .test_clone_ticket import GmpCloneTicketTestCase
from .test_create_schedule import GmpCreateScheduleTestCase
from .test_create_ticket import GmpCreateTicketTestCase
from .test_delete_ticket import GmpDeleteTicketTestCase
from .test_get_ticket import GmpGetTicketTestCase
from .test_get_tickets import GmpGetTargetsTestCase
from .test_get_vulnerabilities import GmpGetVulnerabilitiesTestCase
from .test_get_vulnerability import GmpGetVulnerabilityTestCase
from .test_modify_schedule import GmpModifyScheduleTestCase
from .test_protocol_version import GmpProtocolVersionTestCase
from .test_authenticate import GmpAuthenticateTestCase
from .test_clone_report_format import GmpCloneReportFormatTestCase
from .test_clone_credential import GmpCloneCredentialTestCase
from .test_clone_filter import GmpCloneFilterTestCase
from .test_clone_group import GmpCloneGroupTestCase
from .test_clone_permission import GmpClonePermissionTestCase
from .test_clone_role import GmpCloneRoleTestCase
from .test_clone_scanner import GmpCloneScannerTestCase
from .test_clone_schedule import GmpCloneScheduleTestCase
from .test_clone_tag import GmpCloneTagTestCase
from .test_clone_user import GmpCloneUserTestCase
from .test_create_group import GmpCreateGroupTestCase
from .test_create_role import GmpCreateRoleTestCase
from .test_create_user import GmpCreateUserTestCase
from .test_delete_credential import GmpDeleteCredentialTestCase
from .test_delete_filter import GmpDeleteFilterTestCase
from .test_delete_group import GmpDeleteGroupTestCase
from .test_delete_permission import GmpDeletePermissionTestCase
from .test_delete_report_format import GmpDeleteReportFormatTestCase
from .test_delete_role import GmpDeleteRoleTestCase
from .test_delete_scanner import GmpDeleteScannerTestCase
from .test_delete_schedule import GmpDeleteScheduleTestCase
from .test_delete_tag import GmpDeleteTagTestCase
from .test_delete_user import GmpDeleteUserTestCase
from .test_describe_auth import GmpDescribeAuthCommandTestCase
from .test_empty_trashcan import GmpEmptyTrashcanCommandTestCase
from .test_get_credential import GmpGetCredentialTestCase
from .test_get_credentials import GmpGetCredentialsTestCase
from .test_get_feeds import GmpGetFeedsTestCase
from .test_get_filter import GmpGetFilterTestCase
from .test_get_filters import GmpGetFiltersTestCase
from .test_get_group import GmpGetGroupTestCase
from .test_get_groups import GmpGetGroupsTestCase
from .test_get_permission import GmpGetPermissionTestCase
from .test_get_permissions import GmpGetPermissionsTestCase
from .test_get_preference import GmpGetPreferenceTestCase
from .test_get_preferences import GmpGetPreferencesTestCase
from .test_get_report_format import GmpGetReportFormatTestCase
from .test_get_report_formats import GmpGetReportFormatsTestCase
from .test_get_role import GmpGetRoleTestCase
from .test_get_roles import GmpGetRolesTestCase
from .test_get_scanner import GmpGetScannerTestCase
from .test_get_scanners import GmpGetScannersTestCase
from .test_get_schedule import GmpGetScheduleTestCase
from .test_get_schedules import GmpGetSchedulesTestCase
from .test_get_setting import GmpGetSettingTestCase
from .test_get_settings import GmpGetSettingsTestCase
from .test_get_system_reports import GmpGetSystemReportsTestCase
from .test_get_tag import GmpGetTagTestCase
from .test_get_tags import GmpGetTagsTestCase
from .test_get_user import GmpGetUserTestCase
from .test_get_users import GmpGetUsersTestCase
from .test_get_version import GmpGetVersionCommandTestCase
from .test_help import GmpHelpTestCase
from .test_import_config import GmpImportConfigTestCase
from .test_import_report_format import GmpImportReportFormatTestCase
from .test_modify_auth import GmpModifyAuthTestCase
from .test_modify_config import GmpModifyConfigTestCase
from .test_modify_config_set_comment import GmpModifyConfigSetCommentTestCase
from .test_modify_config_set_name import GmpModifyConfigSetNameTestCase
from .test_modify_config_set_family_selection import (
    GmpModifyConfigSetFamilySelectionTestCase,
)
from .test_modify_config_set_nvt_preference import (
    GmpModifyConfigSetNvtPreferenceTestCase,
)
from .test_modify_config_set_nvt_selection import (
    GmpModifyConfigSetNvtSelectionTestCase,
)
from .test_modify_config_set_scanner_preference import (
    GmpModifyConfigSetScannerPreferenceTestCase,
)
from .test_modify_group import GmpModifyGroupTestCase
from .test_modify_role import GmpModifyRoleTestCase
from .test_modify_setting import GmpModifySettingTestCase
from .test_modify_user import GmpModifyUserTestCase
from .test_restore import GmpRestoreTestCase
from .test_sync_cert import GmpSyncCertCommandTestCase
from .test_sync_config import GmpSyncConfigCommandTestCase
from .test_sync_feed import GmpSyncFeedCommandTestCase
from .test_sync_scap import GmpSyncScapCommandTestCase
from .test_verify_report_format import GmpVerifyReportFormatTestCase
from .test_verify_scanner import GmpVerifyScannerTestCase
from .test_with_statement import GmpWithStatementTestCase
