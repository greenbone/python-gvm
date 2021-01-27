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
from ..gmpv9.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv214CloneAuditTestCase(GmpCloneAuditTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv214TestCase):
    pass


class Gmpv214ClonePolicyTestCase(GmpClonePolicyTestCase, Gmpv214TestCase):

    pass


class Gmpv214CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv214TestCase):
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


class Gmpv214CreateTaskCommandTestCase(
    GmpCreateTaskCommandTestCase, Gmpv214TestCase
):
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


class Gmpv214DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv214TestCase):
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


class Gmpv214GetTaskTestCase(GmpGetTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTasksTestCase(GmpGetTasksTestCase, Gmpv214TestCase):

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


class Gmpv214ImportReportTestCase(GmpImportReportTestCase, Gmpv214TestCase):
    pass
