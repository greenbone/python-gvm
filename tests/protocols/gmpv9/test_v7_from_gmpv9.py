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

from . import Gmpv9TestCase
from ..gmpv7.testcmds import *  # pylint: disable=unused-wildcard-import, wildcard-import


class Gmpv9AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneAgentTestCase(GmpCloneAgentTestCase, Gmpv9TestCase):

    pass


class Gmpv9CloneAlertTestCase(GmpCloneAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneCredentialTestCase(GmpCloneCredentialTestCase, Gmpv9TestCase):

    pass


class Gmpv9HelpTestCase(GmpHelpTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneNoteTestCase(GmpCloneNoteTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneOverrideTestCase(GmpCloneOverrideTestCase, Gmpv9TestCase):
    pass


class Gmpv9ClonePermissionTestCase(GmpClonePermissionTestCase, Gmpv9TestCase):
    pass


class Gmpv9ClonePortListTestCase(GmpClonePortListTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneScannerTestCase(GmpCloneScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneTagTestCase(GmpCloneTagTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneTargetCommandTestCase(
    GmpCloneTargetCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneUserTestCase(GmpCloneUserTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateAgentTestCase(GmpCreateAgentTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateContainerTaskCommandTestCase(
    GMPCreateContainerTaskCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateHostTestCase(GmpCreateHostTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateNoteTestCase(GmpCreateNoteTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateOverrideTestCase(GmpCreateOverrideTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreatePortListTestCase(GmpCreatePortListTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreatePortRangeTestCase(GmpCreatePortRangeTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateUserTestCase(GmpCreateUserTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteAgentTestCase(GmpDeleteAgentTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteAlertTestCase(GmpDeleteAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteAssetTestCase(GmpDeleteAssetTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteCredentialTestCase(GmpDeleteCredentialTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteNoteTestCase(GmpDeleteNoteTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteOverrideTestCase(GmpDeleteOverrideTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeletePermissionTestCase(GmpDeletePermissionTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeletePortListTestCase(GmpDeletePortListTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeletePortRangeTestCase(GmpDeletePortRangeTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteReportTestCase(GmpDeleteReportTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv9TestCase
):
    pass


class Gmpv9DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteScannerTestCase(GmpDeleteScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTagTestCase(GmpDeleteTagTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTargetTestCase(GmpDeleteTargetTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteUserTestCase(GmpDeleteUserTestCase, Gmpv9TestCase):
    pass


class Gmpv9DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9GetAgentTestCase(GmpGetAgentTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAgentsTestCase(GmpGetAgentsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAlertTestCase(GmpGetAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAlertsTestCase(GmpGetAlertsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAssetTestCase(GmpGetAssetTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAssetsTestCase(GmpGetAssetsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetCredentialTestCase(GmpGetCredentialTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetCredentialsTestCase(GmpGetCredentialsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetFeedTestCase(GmpGetFeedTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetFeedsTestCase(GmpGetFeedsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetFilterTestCase(GmpGetFilterTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetGroupTestCase(GmpGetGroupTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetInfoTestCase(GmpGetInfoTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetNoteTestCase(GmpGetNoteTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetNotesTestCase(GmpGetNotesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetNvtTestCase(GmpGetNvtTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetNvtFamiliesTestCase(GmpGetNvtFamiliesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetNvtsTestCase(GmpGetNvtsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetOverrideTestCase(GmpGetOverrideTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetOverridesTestCase(GmpGetOverridesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPermissionTestCase(GmpGetPermissionTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPermissionsTestCase(GmpGetPermissionsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPortListTestCase(GmpGetPortListTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPortListsTestCase(GmpGetPortListsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPreferenceTestCase(GmpGetPreferenceTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPreferencesTestCase(GmpGetPreferencesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetReportTestCase(GmpGetReportTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetReportFormatTestCase(GmpGetReportFormatTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetReportFormatsTestCase(GmpGetReportFormatsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetReportsTestCase(GmpGetReportsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetResultTestCase(GmpGetResultTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetResultsTestCase(GmpGetResultsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetRoleTestCase(GmpGetRoleTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetRolesTestCase(GmpGetRolesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetScannerTestCase(GmpGetScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetScannersTestCase(GmpGetScannersTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetScheduleTestCase(GmpGetScheduleTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetSchedulesTestCase(GmpGetSchedulesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetSettingTestCase(GmpGetSettingTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetSettingsTestCase(GmpGetSettingsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetSystemReportsTestCase(GmpGetSystemReportsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTagTestCase(GmpGetTagTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTagsTestCase(GmpGetTagsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTargetTestCase(GmpGetTargetTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetUserTestCase(GmpGetUserTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetUsersTestCase(GmpGetUsersTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ImportConfigTestCase(GmpImportConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9ImportReportTestCase(GmpImportReportTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyAgentTestCase(GmpModifyAgentTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyAssetTestCase(GmpModifyAssetTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyConfigTestCase(GmpModifyConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyConfigSetCommentTestCase(
    GmpModifyConfigSetCommentTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyConfigSetFamilySelectionTestCase(
    GmpModifyConfigSetFamilySelectionTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyConfigSetNvtPreferenceTestCase(
    GmpModifyConfigSetNvtPreferenceTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyConfigSetNvtSelectionTestCase(
    GmpModifyConfigSetNvtSelectionTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyConfigSetScannerPreferenceTestCase(
    GmpModifyConfigSetScannerPreferenceTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyNoteTestCase(GmpModifyNoteTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyOverrideTestCase(GmpModifyOverrideTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyPortListTestCase(GmpModifyPortListTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifySettingTestCase(GmpModifySettingTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyTargetTestCase(GmpModifyTargetTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyTaskCommandTestCase(
    GmpModifyTaskCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyUserTestCase(GmpModifyUserTestCase, Gmpv9TestCase):
    pass


class Gmpv9MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9RestoreTestCase(GmpRestoreTestCase, Gmpv9TestCase):
    pass


class Gmpv9ResumeTaskTestCase(GmpResumeTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9StartTaskTestCase(GmpStartTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9StopTaskTestCase(GmpStopTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9SyncCertCommandTestCase(GmpSyncCertCommandTestCase, Gmpv9TestCase):
    pass


class Gmpv9SyncConfigCommandTestCase(
    GmpSyncConfigCommandTestCase, Gmpv9TestCase
):

    pass


class Gmpv9SyncFeedCommandTestCase(GmpSyncFeedCommandTestCase, Gmpv9TestCase):
    pass


class Gmpv9SyncScapCommandTestCase(GmpSyncScapCommandTestCase, Gmpv9TestCase):
    pass


class Gmpv9TestAlertTestCase(GmpTestAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9TriggerAlertTestCase(GmpTriggerAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9VerifyAgentTestCase(GmpVerifyAgentTestCase, Gmpv9TestCase):
    pass


class Gmpv9VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv9TestCase
):
    pass


class Gmpv9v7VerifyScannerTestCase(GmpVerifyScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv9TestCase):
    pass
