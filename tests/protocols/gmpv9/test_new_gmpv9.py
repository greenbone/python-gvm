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
from .testcmds import *  # pylint: disable=wildcard-import


class Gmpv9CloneAuditTestCase(GmpCloneAuditTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneConfigTestCase(GmpCloneConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9ClonePolicyTestCase(GmpClonePolicyTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyAlertTestCase(GmpModifyAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateAlertTestCase(GmpCreateAlertTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateAuditCommandTestCase(
    GmpCreateAuditCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateConfigTestCase(GmpCreateConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateConfigFromOSPScannerTestCase(
    GmpCreateConfigFromOSPScannerTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateCredentialTestCase(GmpCreateCredentialTestCase, Gmpv9TestCase):

    pass


class Gmpv9CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreatePermissionTestCase(GmpCreatePermissionTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreatePolicyTestCase(GmpCreatePolicyTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateTagTestCase(GmpCreateTagTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateTaskCommandTestCase(
    GmpCreateTaskCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestCase, Gmpv9TestCase
):
    pass


class Gmpv9DeleteAuditTestCase(GmpDeleteAuditTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteConfigTestCase(GmpDeleteConfigTestCase, Gmpv9TestCase):

    pass


class Gmpv9DeletePolicyTestCase(GmpDeletePolicyTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestCase, Gmpv9TestCase
):
    pass


class Gmpv9GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv9TestCase):

    pass


class Gmpv9GetAuditTestCase(GmpGetAuditTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetAuditsTestCase(GmpGetAuditsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetConfigTestCase(GmpGetConfigTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetConfigsTestCase(GmpGetConfigsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPoliciesTestCase(GmpGetPoliciesTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetPolicyTestCase(GmpGetPolicyTestCase, Gmpv9TestCase):

    pass


class Gmpv9GetTaskTestCase(GmpGetTaskTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTasksTestCase(GmpGetTasksTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTlsCertificateTestCase(
    GmpGetTlsCertificateTestCase, Gmpv9TestCase
):
    pass


class Gmpv9GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyAuditCommandTestCase(
    GmpModifyAuditCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyCredentialTestCase(GmpModifyCredentialTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyPermissionTestCase(GmpModifyPermissionTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv9TestCase
):
    pass


class Gmpv9ModifyTagTestCase(GmpModifyTagTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv9TestCase):
    pass
