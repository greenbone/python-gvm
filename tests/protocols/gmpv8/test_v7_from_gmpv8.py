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

from . import Gmpv8TestCase
from ..gmpv7.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv8AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneAgentTestCase(GmpCloneAgentTestCase, Gmpv8TestCase):

    pass


class Gmpv8CloneAlertTestCase(GmpCloneAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv8TestCase
):
    pass


class Gmpv8CloneCredentialTestCase(GmpCloneCredentialTestCase, Gmpv8TestCase):

    pass


class Gmpv8CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneNoteTestCase(GmpCloneNoteTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneOverrideTestCase(GmpCloneOverrideTestCase, Gmpv8TestCase):
    pass


class Gmpv8ClonePermissionTestCase(GmpClonePermissionTestCase, Gmpv8TestCase):
    pass


class Gmpv8ClonePortListTestCase(GmpClonePortListTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneScannerTestCase(GmpCloneScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneTagTestCase(GmpCloneTagTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneTargetCommandTestCase(
    GmpCloneTargetCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8CloneUserTestCase(GmpCloneUserTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateAgentTestCase(GmpCreateAgentTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateConfigTestCase(GmpCreateConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateContainerTaskCommandTestCase(
    GMPCreateContainerTaskCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateHostTestCase(GmpCreateHostTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateNoteTestCase(GmpCreateNoteTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateOverrideTestCase(GmpCreateOverrideTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreatePortListTestCase(GmpCreatePortListTestCase, Gmpv8TestCase):
    pass


class Gmpv8HelpTestCase(GmpHelpTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreatePortRangeTestCase(GmpCreatePortRangeTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateTaskCommandTestCase(
    GmpCreateTaskCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8CreateUserTestCase(GmpCreateUserTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteAgentTestCase(GmpDeleteAgentTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteAlertTestCase(GmpDeleteAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteAssetTestCase(GmpDeleteAssetTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteConfigTestCase(GmpDeleteConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteCredentialTestCase(GmpDeleteCredentialTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteNoteTestCase(GmpDeleteNoteTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteOverrideTestCase(GmpDeleteOverrideTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeletePermissionTestCase(GmpDeletePermissionTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeletePortListTestCase(GmpDeletePortListTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeletePortRangeTestCase(GmpDeletePortRangeTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteReportTestCase(GmpDeleteReportTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv8TestCase
):
    pass


class Gmpv8DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteScannerTestCase(GmpDeleteScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteTagTestCase(GmpDeleteTagTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteTargetTestCase(GmpDeleteTargetTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteUserTestCase(GmpDeleteUserTestCase, Gmpv8TestCase):
    pass


class Gmpv8DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8GetAgentTestCase(GmpGetAgentTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetAgentsTestCase(GmpGetAgentsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetAlertTestCase(GmpGetAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetAlertsTestCase(GmpGetAlertsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetAssetTestCase(GmpGetAssetTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetAssetsTestCase(GmpGetAssetsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetConfigTestCase(GmpGetConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetConfigsTestCase(GmpGetConfigsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetCredentialTestCase(GmpGetCredentialTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetCredentialsTestCase(GmpGetCredentialsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetFeedTestCase(GmpGetFeedTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetFeedsTestCase(GmpGetFeedsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetFilterTestCase(GmpGetFilterTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetGroupTestCase(GmpGetGroupTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetInfoTestCase(GmpGetInfoTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetNoteTestCase(GmpGetNoteTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetNotesTestCase(GmpGetNotesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetNvtTestCase(GmpGetNvtTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetNvtFamiliesTestCase(GmpGetNvtFamiliesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetNvtsTestCase(GmpGetNvtsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetOverrideTestCase(GmpGetOverrideTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetOverridesTestCase(GmpGetOverridesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPermissionTestCase(GmpGetPermissionTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPermissionsTestCase(GmpGetPermissionsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPortListTestCase(GmpGetPortListTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPortListsTestCase(GmpGetPortListsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPreferenceTestCase(GmpGetPreferenceTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetPreferencesTestCase(GmpGetPreferencesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetReportTestCase(GmpGetReportTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetReportFormatTestCase(GmpGetReportFormatTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetReportFormatsTestCase(GmpGetReportFormatsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetReportsTestCase(GmpGetReportsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetResultTestCase(GmpGetResultTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetResultsTestCase(GmpGetResultsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetRoleTestCase(GmpGetRoleTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetRolesTestCase(GmpGetRolesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetScannerTestCase(GmpGetScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetScannersTestCase(GmpGetScannersTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetScheduleTestCase(GmpGetScheduleTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetSchedulesTestCase(GmpGetSchedulesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetSettingTestCase(GmpGetSettingTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetSettingsTestCase(GmpGetSettingsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetSystemReportsTestCase(GmpGetSystemReportsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTagTestCase(GmpGetTagTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTagsTestCase(GmpGetTagsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTargetTestCase(GmpGetTargetTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTaskTestCase(GmpGetTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTasksTestCase(GmpGetTasksTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetUserTestCase(GmpGetUserTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetUsersTestCase(GmpGetUsersTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ImportConfigTestCase(GmpImportConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ImportReportTestCase(GmpImportReportTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyAgentTestCase(GmpModifyAgentTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyAssetTestCase(GmpModifyAssetTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyConfigTestCase(GmpModifyConfigTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyConfigSetCommentTestCase(
    GmpModifyConfigSetCommentTestCase, Gmpv8TestCase
):
    pass


class Gmpv7ModifyConfigSetNameTestCase(
    GmpModifyConfigSetNameTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyConfigSetFamilySelectionTestCase(
    GmpModifyConfigSetFamilySelectionTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyConfigSetNvtPreferenceTestCase(
    GmpModifyConfigSetNvtPreferenceTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyConfigSetNvtSelectionTestCase(
    GmpModifyConfigSetNvtSelectionTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyConfigSetScannerPreferenceTestCase(
    GmpModifyConfigSetScannerPreferenceTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyNoteTestCase(GmpModifyNoteTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyOverrideTestCase(GmpModifyOverrideTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyPortListTestCase(GmpModifyPortListTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifySettingTestCase(GmpModifySettingTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyTargetTestCase(GmpModifyTargetTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyTaskCommandTestCase(
    GmpModifyTaskCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyUserTestCase(GmpModifyUserTestCase, Gmpv8TestCase):
    pass


class Gmpv8MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8RestoreTestCase(GmpRestoreTestCase, Gmpv8TestCase):
    pass


class Gmpv8ResumeTaskTestCase(GmpResumeTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8StartTaskTestCase(GmpStartTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8StopTaskTestCase(GmpStopTaskTestCase, Gmpv8TestCase):
    pass


class Gmpv8SyncCertCommandTestCase(GmpSyncCertCommandTestCase, Gmpv8TestCase):
    pass


class Gmpv8SyncConfigCommandTestCase(
    GmpSyncConfigCommandTestCase, Gmpv8TestCase
):

    pass


class Gmpv8SyncFeedCommandTestCase(GmpSyncFeedCommandTestCase, Gmpv8TestCase):
    pass


class Gmpv8SyncScapCommandTestCase(GmpSyncScapCommandTestCase, Gmpv8TestCase):
    pass


class Gmpv8TestAlertTestCase(GmpTestAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8TriggerAlertTestCase(GmpTriggerAlertTestCase, Gmpv8TestCase):
    pass


class Gmpv8VerifyAgentTestCase(GmpVerifyAgentTestCase, Gmpv8TestCase):
    pass


class Gmpv8VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv8TestCase
):
    pass


class Gmpv8v7VerifyScannerTestCase(GmpVerifyScannerTestCase, Gmpv8TestCase):
    pass


class Gmpv8v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv8TestCase):
    pass
