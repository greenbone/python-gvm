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

from . import Gmpv208TestCase
from .testcmds import *  # pylint: disable=unused-wildcard-import, wildcard-import


class Gmpv208CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreatePermissionTestCase(
    GmpCreatePermissionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateTagTestCase(GmpCreateTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyPermissionTestCase(
    GmpModifyPermissionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyTagTestCase(GmpModifyTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetFeedTestCase(GmpGetFeedTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneAuditTestCase(GmpCloneAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208ClonePolicyTestCase(GmpClonePolicyTestCase, Gmpv208TestCase):

    pass


class Gmpv208CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateAuditCommandTestCase(
    GmpCreateAuditCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateConfigTestCase(GmpCreateConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateConfigFromOSPScannerTestCase(
    GmpCreateConfigFromOSPScannerTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateCredentialTestCase(
    GmpCreateCredentialTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreatePolicyTestCase(GmpCreatePolicyTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestCase, Gmpv208TestCase
):

    pass


class Gmpv208DeleteAuditTestCase(GmpDeleteAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteConfigTestCase(GmpDeleteConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeletePolicyTestCase(GmpDeletePolicyTestCase, Gmpv208TestCase):

    pass


class Gmpv208DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetAuditTestCase(GmpGetAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetAuditsTestCase(GmpGetAuditsTestCase, Gmpv208TestCase):

    pass


class Gmpv208GetConfigTestCase(GmpGetConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetConfigsTestCase(GmpGetConfigsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPoliciesTestCase(GmpGetPoliciesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPolicyTestCase(GmpGetPolicyTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTlsCertificateTestCase(
    GmpGetTlsCertificateTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyAuditCommandTestCase(
    GmpModifyAuditCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyCredentialTestCase(
    GmpModifyCredentialTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208ResumeAuditTestCase(GmpResumeAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208StartAuditTestCase(GmpStartAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208StopAuditTestCase(GmpStopAuditTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneTicketTestCase(GmpCloneTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv208TestCase):

    pass


class Gmpv208CreateTicketTestCase(GmpCreateTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteTicketTestCase(GmpDeleteTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTicketTestCase(GmpGetTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneAlertTestCase(GmpCloneAlertTestCase, Gmpv208TestCase):

    pass


class Gmpv208CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CloneCredentialTestCase(
    GmpCloneCredentialTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208HelpTestCase(GmpHelpTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv208TestCase):

    pass


class Gmpv208CloneNoteTestCase(GmpCloneNoteTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneOverrideTestCase(GmpCloneOverrideTestCase, Gmpv208TestCase):
    pass


class Gmpv208ClonePermissionTestCase(
    GmpClonePermissionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneScannerTestCase(GmpCloneScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneTagTestCase(GmpCloneTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneUserTestCase(GmpCloneUserTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateHostTestCase(GmpCreateHostTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateNoteTestCase(GmpCreateNoteTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateOverrideTestCase(GmpCreateOverrideTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateUserTestCase(GmpCreateUserTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteAlertTestCase(GmpDeleteAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteAssetTestCase(GmpDeleteAssetTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteCredentialTestCase(
    GmpDeleteCredentialTestCase, Gmpv208TestCase
):
    pass


class Gmpv208DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteNoteTestCase(GmpDeleteNoteTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteOverrideTestCase(GmpDeleteOverrideTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeletePermissionTestCase(
    GmpDeletePermissionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteScannerTestCase(GmpDeleteScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteTagTestCase(GmpDeleteTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteUserTestCase(GmpDeleteUserTestCase, Gmpv208TestCase):
    pass


class Gmpv208DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetAlertTestCase(GmpGetAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetAlertsTestCase(GmpGetAlertsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetAssetTestCase(GmpGetAssetTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetAssetsTestCase(GmpGetAssetsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetCredentialTestCase(GmpGetCredentialTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetCredentialsTestCase(GmpGetCredentialsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetFeedsTestCase(GmpGetFeedsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetFilterTestCase(GmpGetFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetGroupTestCase(GmpGetGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetNoteTestCase(GmpGetNoteTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetNotesTestCase(GmpGetNotesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetOverrideTestCase(GmpGetOverrideTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetOverridesTestCase(GmpGetOverridesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPermissionTestCase(GmpGetPermissionTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPermissionsTestCase(GmpGetPermissionsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPreferenceTestCase(GmpGetPreferenceTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetPreferencesTestCase(GmpGetPreferencesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetReportFormatTestCase(
    GmpGetReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetReportFormatsTestCase(
    GmpGetReportFormatsTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetRoleTestCase(GmpGetRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetRolesTestCase(GmpGetRolesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetScannerTestCase(GmpGetScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetScannersTestCase(GmpGetScannersTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetScheduleTestCase(GmpGetScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetSchedulesTestCase(GmpGetSchedulesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetSettingTestCase(GmpGetSettingTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetSettingsTestCase(GmpGetSettingsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetSystemReportsTestCase(
    GmpGetSystemReportsTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetTagTestCase(GmpGetTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTagsTestCase(GmpGetTagsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetUserTestCase(GmpGetUserTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetUsersTestCase(GmpGetUsersTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ImportConfigTestCase(GmpImportConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyAssetTestCase(GmpModifyAssetTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyConfigTestCase(GmpModifyConfigTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyConfigSetCommentTestCase(
    GmpModifyConfigSetCommentTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyConfigSetFamilySelectionTestCase(
    GmpModifyConfigSetFamilySelectionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyConfigSetNvtPreferenceTestCase(
    GmpModifyConfigSetNvtPreferenceTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyConfigSetNvtSelectionTestCase(
    GmpModifyConfigSetNvtSelectionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyConfigSetScannerPreferenceTestCase(
    GmpModifyConfigSetScannerPreferenceTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyNoteTestCase(GmpModifyNoteTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyOverrideTestCase(GmpModifyOverrideTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifySettingTestCase(GmpModifySettingTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyUserTestCase(GmpModifyUserTestCase, Gmpv208TestCase):
    pass


class Gmpv208RestoreTestCase(GmpRestoreTestCase, Gmpv208TestCase):
    pass


class Gmpv208SyncCertCommandTestCase(
    GmpSyncCertCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208SyncConfigCommandTestCase(
    GmpSyncConfigCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208SyncFeedCommandTestCase(
    GmpSyncFeedCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208SyncScapCommandTestCase(
    GmpSyncScapCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208TestAlertTestCase(GmpTestAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208TriggerAlertTestCase(GmpTriggerAlertTestCase, Gmpv208TestCase):
    pass


class Gmpv208VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208v7VerifyScannerTestCase(GmpVerifyScannerTestCase, Gmpv208TestCase):
    pass


class Gmpv208v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv208TestCase):
    pass
