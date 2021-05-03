# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from . import Gmpv214TestCase
from ..gmpv208.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv214CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreatePermissionTestCase(
    GmpCreatePermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateTagTestCase(GmpCreateTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetInfoTestCase(GmpGetInfoTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyPermissionTestCase(
    GmpModifyPermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyTagTestCase(GmpModifyTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetFeedTestCase(GmpGetFeedTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneAuditTestCase(GmpCloneAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214ClonePolicyTestCase(GmpClonePolicyTestCase, Gmpv214TestCase):

    pass


class Gmpv214CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateAuditCommandTestCase(
    GmpCreateAuditCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateConfigTestCase(GmpCreateConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateConfigFromOSPScannerTestCase(
    GmpCreateConfigFromOSPScannerTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateCredentialTestCase(
    GmpCreateCredentialTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreatePolicyTestCase(GmpCreatePolicyTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestCase, Gmpv214TestCase
):

    pass


class Gmpv214DeleteAuditTestCase(GmpDeleteAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteConfigTestCase(GmpDeleteConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeletePolicyTestCase(GmpDeletePolicyTestCase, Gmpv214TestCase):

    pass


class Gmpv214DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetAuditTestCase(GmpGetAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAuditsTestCase(GmpGetAuditsTestCase, Gmpv214TestCase):

    pass


class Gmpv214GetConfigTestCase(GmpGetConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetConfigsTestCase(GmpGetConfigsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPoliciesTestCase(GmpGetPoliciesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPolicyTestCase(GmpGetPolicyTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTlsCertificateTestCase(
    GmpGetTlsCertificateTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyAuditCommandTestCase(
    GmpModifyAuditCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyCredentialTestCase(
    GmpModifyCredentialTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ResumeAuditTestCase(GmpResumeAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214StartAuditTestCase(GmpStartAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214StopAuditTestCase(GmpStopAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneTicketTestCase(GmpCloneTicketTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv214TestCase):

    pass


class Gmpv214CreateTicketTestCase(GmpCreateTicketTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteTicketTestCase(GmpDeleteTicketTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTicketTestCase(GmpGetTicketTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneAlertTestCase(GmpCloneAlertTestCase, Gmpv214TestCase):

    pass


class Gmpv214CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CloneCredentialTestCase(
    GmpCloneCredentialTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214HelpTestCase(GmpHelpTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv214TestCase):

    pass


class Gmpv214CloneNoteTestCase(GmpCloneNoteTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneOverrideTestCase(GmpCloneOverrideTestCase, Gmpv214TestCase):
    pass


class Gmpv214ClonePermissionTestCase(
    GmpClonePermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ClonePortListTestCase(GmpClonePortListTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneScannerTestCase(GmpCloneScannerTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneTagTestCase(GmpCloneTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneTargetCommandTestCase(
    GmpCloneTargetCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CloneUserTestCase(GmpCloneUserTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateHostTestCase(GmpCreateHostTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreatePortListTestCase(GmpCreatePortListTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreatePortRangeTestCase(
    GmpCreatePortRangeTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateUserTestCase(GmpCreateUserTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteAlertTestCase(GmpDeleteAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteAssetTestCase(GmpDeleteAssetTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteCredentialTestCase(
    GmpDeleteCredentialTestCase, Gmpv214TestCase
):
    pass


class Gmpv214DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteNoteTestCase(GmpDeleteNoteTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteOverrideTestCase(GmpDeleteOverrideTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeletePermissionTestCase(
    GmpDeletePermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214DeletePortListTestCase(GmpDeletePortListTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeletePortRangeTestCase(
    GmpDeletePortRangeTestCase, Gmpv214TestCase
):
    pass


class Gmpv214DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteScannerTestCase(GmpDeleteScannerTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteTagTestCase(GmpDeleteTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteTargetTestCase(GmpDeleteTargetTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteUserTestCase(GmpDeleteUserTestCase, Gmpv214TestCase):
    pass


class Gmpv214DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetAlertTestCase(GmpGetAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAlertsTestCase(GmpGetAlertsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAssetTestCase(GmpGetAssetTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAssetsTestCase(GmpGetAssetsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetCredentialTestCase(GmpGetCredentialTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetCredentialsTestCase(GmpGetCredentialsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetFeedsTestCase(GmpGetFeedsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetFilterTestCase(GmpGetFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetGroupTestCase(GmpGetGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetNoteTestCase(GmpGetNoteTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetNotesTestCase(GmpGetNotesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetNvtTestCase(GmpGetNvtTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetNvtFamiliesTestCase(GmpGetNvtFamiliesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetNvtsTestCase(GmpGetNvtsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetOverrideTestCase(GmpGetOverrideTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetOverridesTestCase(GmpGetOverridesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPermissionTestCase(GmpGetPermissionTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPermissionsTestCase(GmpGetPermissionsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPortListTestCase(GmpGetPortListTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPortListsTestCase(GmpGetPortListsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPreferenceTestCase(GmpGetPreferenceTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetPreferencesTestCase(GmpGetPreferencesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetReportFormatTestCase(
    GmpGetReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetReportFormatsTestCase(
    GmpGetReportFormatsTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetResultTestCase(GmpGetResultTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetResultsTestCase(GmpGetResultsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetRoleTestCase(GmpGetRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetRolesTestCase(GmpGetRolesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetScannerTestCase(GmpGetScannerTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetScannersTestCase(GmpGetScannersTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetScheduleTestCase(GmpGetScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetSchedulesTestCase(GmpGetSchedulesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetSettingTestCase(GmpGetSettingTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetSettingsTestCase(GmpGetSettingsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetSystemReportsTestCase(
    GmpGetSystemReportsTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetTagTestCase(GmpGetTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTagsTestCase(GmpGetTagsTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTargetTestCase(GmpGetTargetTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetUserTestCase(GmpGetUserTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetUsersTestCase(GmpGetUsersTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ImportConfigTestCase(GmpImportConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyAssetTestCase(GmpModifyAssetTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyConfigTestCase(GmpModifyConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyConfigSetCommentTestCase(
    GmpModifyConfigSetCommentTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyConfigSetFamilySelectionTestCase(
    GmpModifyConfigSetFamilySelectionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyConfigSetNvtPreferenceTestCase(
    GmpModifyConfigSetNvtPreferenceTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyConfigSetNvtSelectionTestCase(
    GmpModifyConfigSetNvtSelectionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyConfigSetScannerPreferenceTestCase(
    GmpModifyConfigSetScannerPreferenceTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyPortListTestCase(GmpModifyPortListTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifySettingTestCase(GmpModifySettingTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyTargetTestCase(GmpModifyTargetTestCase, Gmpv214TestCase):
    pass


class Gmpv214RestoreTestCase(GmpRestoreTestCase, Gmpv214TestCase):
    pass


class Gmpv214SyncCertCommandTestCase(
    GmpSyncCertCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214SyncConfigCommandTestCase(
    GmpSyncConfigCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214SyncFeedCommandTestCase(
    GmpSyncFeedCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214SyncScapCommandTestCase(
    GmpSyncScapCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214TestAlertTestCase(GmpTestAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214TriggerAlertTestCase(GmpTriggerAlertTestCase, Gmpv214TestCase):
    pass


class Gmpv214VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214v7VerifyScannerTestCase(GmpVerifyScannerTestCase, Gmpv214TestCase):
    pass


class Gmpv214v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv214TestCase):
    pass
