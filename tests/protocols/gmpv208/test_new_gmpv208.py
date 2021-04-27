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


class Gmpv208CloneAgentTestCase(GmpCloneAgentTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreatePermissionTestCase(
    GmpCreatePermissionTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateTagTestCase(GmpCreateTagTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateTargetCommandTestCase(
    GmpCreateTargetCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetInfoTestCase(GmpGetInfoTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv208TestCase):
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


class Gmpv208CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv208TestCase):
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


class Gmpv208CreateTaskCommandTestCase(
    GmpCreateTaskCommandTestCase, Gmpv208TestCase
):
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


class Gmpv208DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv208TestCase):
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


class Gmpv208GetTaskTestCase(GmpGetTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTasksTestCase(GmpGetTasksTestCase, Gmpv208TestCase):

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


class Gmpv208ImportReportTestCase(GmpImportReportTestCase, Gmpv208TestCase):
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


class Gmpv208GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv208TestCase):
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
