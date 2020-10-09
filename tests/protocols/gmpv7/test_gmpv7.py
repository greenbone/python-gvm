# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import Gmpv7TestCase
from .testcmds import *  # pylint: disable=wildcard-import


class Gmpv7AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneAgentTestCase(GmpCloneAgentTestCase, Gmpv7TestCase):

    pass


class Gmpv7CloneAlertTestCase(GmpCloneAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv7TestCase
):
    pass


class Gmpv7CloneCredentialTestCase(GmpCloneCredentialTestCase, Gmpv7TestCase):

    pass


class Gmpv7CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneNoteTestCase(GmpCloneNoteTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneOverrideTestCase(GmpCloneOverrideTestCase, Gmpv7TestCase):
    pass


class Gmpv7ClonePermissionTestCase(GmpClonePermissionTestCase, Gmpv7TestCase):
    pass


class Gmpv7ClonePortListTestCase(GmpClonePortListTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneScannerTestCase(GmpCloneScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneTagTestCase(GmpCloneTagTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneTargetCommandTestCase(
    GmpCloneTargetCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7HelpTestCase(GmpHelpTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7CloneUserTestCase(GmpCloneUserTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateAgentTestCase(GmpCreateAgentTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateConfigTestCase(GmpCreateConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateContainerTaskCommandTestCase(
    GMPCreateContainerTaskCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7CreateCredentialTestCase(GmpCreateCredentialTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateFilterCommandTestCase(
    GmpCreateFilterCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateHostTestCase(GmpCreateHostTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateNoteTestCase(GmpCreateNoteTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateOverrideTestCase(GmpCreateOverrideTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreatePermissionTestCase(GmpCreatePermissionTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreatePortListTestCase(GmpCreatePortListTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreatePortRangeTestCase(GmpCreatePortRangeTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateTagTestCase(GmpCreateTagTestCase, Gmpv7TestCase):
    pass


class Gmpv7CreateTargetCommandTestCase(
    GmpCreateTargetCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7CreateTaskCommandTestCase(
    GmpCreateTaskCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7CreateUserTestCase(GmpCreateUserTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteAgentTestCase(GmpDeleteAgentTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteAlertTestCase(GmpDeleteAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteAssetTestCase(GmpDeleteAssetTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteConfigTestCase(GmpDeleteConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteCredentialTestCase(GmpDeleteCredentialTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteNoteTestCase(GmpDeleteNoteTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteOverrideTestCase(GmpDeleteOverrideTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeletePermissionTestCase(GmpDeletePermissionTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeletePortListTestCase(GmpDeletePortListTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeletePortRangeTestCase(GmpDeletePortRangeTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteReportTestCase(GmpDeleteReportTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv7TestCase
):
    pass


class Gmpv7DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteScannerTestCase(GmpDeleteScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteTagTestCase(GmpDeleteTagTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteTargetTestCase(GmpDeleteTargetTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7DeleteUserTestCase(GmpDeleteUserTestCase, Gmpv7TestCase):
    pass


class Gmpv7DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7GetAgentTestCase(GmpGetAgentTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAgentsTestCase(GmpGetAgentsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAlertTestCase(GmpGetAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAlertsTestCase(GmpGetAlertsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAssetTestCase(GmpGetAssetTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetAssetsTestCase(GmpGetAssetsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetConfigTestCase(GmpGetConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetConfigsTestCase(GmpGetConfigsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetCredentialTestCase(GmpGetCredentialTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetCredentialsTestCase(GmpGetCredentialsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetFeedTestCase(GmpGetFeedTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetFeedsTestCase(GmpGetFeedsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetFilterTestCase(GmpGetFilterTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetGroupTestCase(GmpGetGroupTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetInfoTestCase(GmpGetInfoTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetNoteTestCase(GmpGetNoteTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetNotesTestCase(GmpGetNotesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetNvtTestCase(GmpGetNvtTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetNvtFamiliesTestCase(GmpGetNvtFamiliesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetNvtsTestCase(GmpGetNvtsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetOverrideTestCase(GmpGetOverrideTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetOverridesTestCase(GmpGetOverridesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPermissionTestCase(GmpGetPermissionTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPermissionsTestCase(GmpGetPermissionsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPortListTestCase(GmpGetPortListTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPortListsTestCase(GmpGetPortListsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPreferenceTestCase(GmpGetPreferenceTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetPreferencesTestCase(GmpGetPreferencesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetReportTestCase(GmpGetReportTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetReportFormatTestCase(GmpGetReportFormatTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetReportFormatsTestCase(GmpGetReportFormatsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetReportsTestCase(GmpGetReportsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetResultTestCase(GmpGetResultTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetResultsTestCase(GmpGetResultsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetRoleTestCase(GmpGetRoleTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetRolesTestCase(GmpGetRolesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetScannerTestCase(GmpGetScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetScannersTestCase(GmpGetScannersTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetScheduleTestCase(GmpGetScheduleTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetSchedulesTestCase(GmpGetSchedulesTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetSettingTestCase(GmpGetSettingTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetSettingsTestCase(GmpGetSettingsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetSystemReportsTestCase(GmpGetSystemReportsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTagTestCase(GmpGetTagTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTagsTestCase(GmpGetTagsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTargetTestCase(GmpGetTargetTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTaskTestCase(GmpGetTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetTasksTestCase(GmpGetTasksTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetUserTestCase(GmpGetUserTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetUsersTestCase(GmpGetUsersTestCase, Gmpv7TestCase):
    pass


class Gmpv7GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ImportConfigTestCase(GmpImportConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ImportReportTestCase(GmpImportReportTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyAgentTestCase(GmpModifyAgentTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyAssetTestCase(GmpModifyAssetTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyConfigTestCase(GmpModifyConfigTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyConfigSetCommentTestCase(
    GmpModifyConfigSetCommentTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyConfigSetNameTestCase(
    GmpModifyConfigSetNameTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyConfigSetFamilySelectionTestCase(
    GmpModifyConfigSetFamilySelectionTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyConfigSetNvtPreferenceTestCase(
    GmpModifyConfigSetNvtPreferenceTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyConfigSetNvtSelectionTestCase(
    GmpModifyConfigSetNvtSelectionTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyConfigSetScannerPreferenceTestCase(
    GmpModifyConfigSetScannerPreferenceTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyCredentialTestCase(GmpModifyCredentialTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyNoteTestCase(GmpModifyNoteTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyOverrideTestCase(GmpModifyOverrideTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyPermissionTestCase(GmpModifyPermissionTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyPortListTestCase(GmpModifyPortListTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifySettingTestCase(GmpModifySettingTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyTagTestCase(GmpModifyTagTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyTargetTestCase(GmpModifyTargetTestCase, Gmpv7TestCase):
    pass


class Gmpv7ModifyTaskCommandTestCase(
    GmpModifyTaskCommandTestCase, Gmpv7TestCase
):
    pass


class Gmpv7ModifyUserTestCase(GmpModifyUserTestCase, Gmpv7TestCase):
    pass


class Gmpv7MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7ProtocolVersionTestCase(GmpProtocolVersionTestCase, Gmpv7TestCase):
    pass


class Gmpv7RestoreTestCase(GmpRestoreTestCase, Gmpv7TestCase):
    pass


class Gmpv7ResumeTaskTestCase(GmpResumeTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7StartTaskTestCase(GmpStartTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7StopTaskTestCase(GmpStopTaskTestCase, Gmpv7TestCase):
    pass


class Gmpv7SyncCertCommandTestCase(GmpSyncCertCommandTestCase, Gmpv7TestCase):
    pass


class Gmpv7SyncConfigCommandTestCase(
    GmpSyncConfigCommandTestCase, Gmpv7TestCase
):

    pass


class Gmpv7SyncFeedCommandTestCase(GmpSyncFeedCommandTestCase, Gmpv7TestCase):
    pass


class Gmpv7SyncScapCommandTestCase(GmpSyncScapCommandTestCase, Gmpv7TestCase):
    pass


class Gmpv7TestAlertTestCase(GmpTestAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7TriggerAlertTestCase(GmpTriggerAlertTestCase, Gmpv7TestCase):
    pass


class Gmpv7VerifyAgentTestCase(GmpVerifyAgentTestCase, Gmpv7TestCase):
    pass


class Gmpv7VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv7TestCase
):
    pass


class Gmpv7v7VerifyScannerTestCase(GmpVerifyScannerTestCase, Gmpv7TestCase):
    pass


class Gmpv7v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv7TestCase):
    pass
