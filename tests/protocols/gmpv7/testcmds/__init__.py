# -*- coding utf-8 -*-
# Ctestright  2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier GPL-3.0-or-later
#
# This program is free software you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http//www.gnu.org/licenses/>.

# pylint: disable=no-member

from .test_authenticate import GmpAuthenticateTestCase
from .test_clone_agent import GmpCloneAgentTestCase
from .test_clone_alert import GmpCloneAlertTestCase
from .test_clone_config import GmpCloneConfigTestCase
from .test_clone_report_format import GmpCloneReportFormatTestCase
from .test_clone_credential import GmpCloneCredentialTestCase
from .test_clone_filter import GmpCloneFilterTestCase
from .test_clone_group import GmpCloneGroupTestCase
from .test_clone_note import GmpCloneNoteTestCase
from .test_clone_override import GmpCloneOverrideTestCase
from .test_clone_permission import GmpClonePermissionTestCase
from .test_clone_port_list import GmpClonePortListTestCase
from .test_clone_role import GmpCloneRoleTestCase
from .test_clone_scanner import GmpCloneScannerTestCase
from .test_clone_schedule import GmpCloneScheduleTestCase
from .test_clone_tag import GmpCloneTagTestCase
from .test_clone_target import GmpCloneTargetCommandTestCase
from .test_clone_task import GmpCloneTaskTestCase
from .test_clone_user import GmpCloneUserTestCase
from .test_create_agent import GmpCreateAgentTestCase
from .test_create_alert import GmpCreateAlertTestCase
from .test_create_config import GmpCreateConfigTestCase
from .test_create_container_task import GMPCreateContainerTaskCommandTestCase
from .test_create_credential import GmpCreateCredentialTestCase
from .test_create_filter import GmpCreateFilterCommandTestCase
from .test_create_group import GmpCreateGroupTestCase
from .test_create_host import GmpCreateHostTestCase
from .test_create_note import GmpCreateNoteTestCase
from .test_create_override import GmpCreateOverrideTestCase
from .test_create_permission import GmpCreatePermissionTestCase
from .test_create_port_list import GmpCreatePortListTestCase
from .test_create_port_range import GmpCreatePortRangeTestCase
from .test_create_role import GmpCreateRoleTestCase
from .test_create_scanner import GmpCreateScannerTestCase
from .test_create_schedule import GmpCreateScheduleTestCase
from .test_create_tag import GmpCreateTagTestCase
from .test_create_target import GmpCreateTargetCommandTestCase
from .test_create_task import GmpCreateTaskCommandTestCase
from .test_create_user import GmpCreateUserTestCase
from .test_delete_agent import GmpDeleteAgentTestCase
from .test_delete_alert import GmpDeleteAlertTestCase
from .test_delete_asset import GmpDeleteAssetTestCase
from .test_delete_config import GmpDeleteConfigTestCase
from .test_delete_credential import GmpDeleteCredentialTestCase
from .test_delete_filter import GmpDeleteFilterTestCase
from .test_delete_group import GmpDeleteGroupTestCase
from .test_delete_note import GmpDeleteNoteTestCase
from .test_delete_override import GmpDeleteOverrideTestCase
from .test_delete_permission import GmpDeletePermissionTestCase
from .test_delete_port_list import GmpDeletePortListTestCase
from .test_delete_port_range import GmpDeletePortRangeTestCase
from .test_delete_report import GmpDeleteReportTestCase
from .test_delete_report_format import GmpDeleteReportFormatTestCase
from .test_delete_role import GmpDeleteRoleTestCase
from .test_delete_scanner import GmpDeleteScannerTestCase
from .test_delete_schedule import GmpDeleteScheduleTestCase
from .test_delete_tag import GmpDeleteTagTestCase
from .test_delete_target import GmpDeleteTargetTestCase
from .test_delete_task import GmpDeleteTaskTestCase
from .test_delete_user import GmpDeleteUserTestCase
from .test_describe_auth import GmpDescribeAuthCommandTestCase
from .test_empty_trashcan import GmpEmptyTrashcanCommandTestCase
from .test_get_agent import GmpGetAgentTestCase
from .test_get_agents import GmpGetAgentsTestCase
from .test_get_aggregates import GmpGetAggregatesTestCase
from .test_get_alert import GmpGetAlertTestCase
from .test_get_alerts import GmpGetAlertsTestCase
from .test_get_asset import GmpGetAssetTestCase
from .test_get_assets import GmpGetAssetsTestCase
from .test_get_config import GmpGetConfigTestCase
from .test_get_configs import GmpGetConfigsTestCase
from .test_get_credential import GmpGetCredentialTestCase
from .test_get_credentials import GmpGetCredentialsTestCase
from .test_get_feed import GmpGetFeedTestCase
from .test_get_feeds import GmpGetFeedsTestCase
from .test_get_filter import GmpGetFilterTestCase
from .test_get_filters import GmpGetFiltersTestCase
from .test_get_group import GmpGetGroupTestCase
from .test_get_groups import GmpGetGroupsTestCase
from .test_get_info import GmpGetInfoTestCase
from .test_get_info_list import GmpGetInfoListTestCase
from .test_get_note import GmpGetNoteTestCase
from .test_get_notes import GmpGetNotesTestCase
from .test_get_nvt import GmpGetNvtTestCase
from .test_get_nvt_families import GmpGetNvtFamiliesTestCase
from .test_get_nvts import GmpGetNvtsTestCase
from .test_get_override import GmpGetOverrideTestCase
from .test_get_overrides import GmpGetOverridesTestCase
from .test_get_permission import GmpGetPermissionTestCase
from .test_get_permissions import GmpGetPermissionsTestCase
from .test_get_port_list import GmpGetPortListTestCase
from .test_get_port_lists import GmpGetPortListsTestCase
from .test_get_preference import GmpGetPreferenceTestCase
from .test_get_preferences import GmpGetPreferencesTestCase
from .test_get_report import GmpGetReportTestCase
from .test_get_report_format import GmpGetReportFormatTestCase
from .test_get_report_formats import GmpGetReportFormatsTestCase
from .test_get_reports import GmpGetReportsTestCase
from .test_get_result import GmpGetResultTestCase
from .test_get_results import GmpGetResultsTestCase
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
from .test_get_target import GmpGetTargetTestCase
from .test_get_targets import GmpGetTargetsTestCase
from .test_get_task import GmpGetTaskTestCase
from .test_get_tasks import GmpGetTasksTestCase
from .test_get_user import GmpGetUserTestCase
from .test_get_users import GmpGetUsersTestCase
from .test_get_version import GmpGetVersionCommandTestCase
from .test_help import GmpHelpTestCase
from .test_import_config import GmpImportConfigTestCase
from .test_import_report_format import GmpImportReportFormatTestCase
from .test_import_report import GmpImportReportTestCase
from .test_modify_agent import GmpModifyAgentTestCase
from .test_modify_alert import GmpModifyAlertTestCase
from .test_modify_asset import GmpModifyAssetTestCase
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
from .test_modify_credential import GmpModifyCredentialTestCase
from .test_modify_filter import GmpModifyFilterTestCase
from .test_modify_group import GmpModifyGroupTestCase
from .test_modify_note import GmpModifyNoteTestCase
from .test_modify_override import GmpModifyOverrideTestCase
from .test_modify_permission import GmpModifyPermissionTestCase
from .test_modify_port_list import GmpModifyPortListTestCase
from .test_modify_report_format import GmpModifyReportFormatTestCase
from .test_modify_role import GmpModifyRoleTestCase
from .test_modify_scanner import GmpModifyScannerTestCase
from .test_modify_schedule import GmpModifyScheduleTestCase
from .test_modify_setting import GmpModifySettingTestCase
from .test_modify_tag import GmpModifyTagTestCase
from .test_modify_target import GmpModifyTargetTestCase
from .test_modify_task import GmpModifyTaskCommandTestCase
from .test_modify_user import GmpModifyUserTestCase
from .test_move_task import GmpMoveTaskTestCase
from .test_protocol_version import GmpProtocolVersionTestCase
from .test_restore import GmpRestoreTestCase
from .test_resume_task import GmpResumeTaskTestCase
from .test_start_task import GmpStartTaskTestCase
from .test_stop_task import GmpStopTaskTestCase
from .test_sync_cert import GmpSyncCertCommandTestCase
from .test_sync_config import GmpSyncConfigCommandTestCase
from .test_sync_feed import GmpSyncFeedCommandTestCase
from .test_sync_scap import GmpSyncScapCommandTestCase
from .test_test_alert import GmpTestAlertTestCase
from .test_trigger_alert import GmpTriggerAlertTestCase
from .test_verify_agent import GmpVerifyAgentTestCase
from .test_verify_report_format import GmpVerifyReportFormatTestCase
from .test_verify_scanner import GmpVerifyScannerTestCase
from .test_with_statement import GmpWithStatementTestCase
