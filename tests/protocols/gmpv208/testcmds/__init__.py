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

from .test_agent_deprecation import GmpCloneAgentTestCase
from .test_create_filter import GmpCreateFilterTestCase
from .test_create_permission import GmpCreatePermissionTestCase
from .test_create_tag import GmpCreateTagTestCase
from .test_create_target import GmpCreateTargetCommandTestCase
from .test_get_aggregates import GmpGetAggregatesTestCase
from .test_get_info import GmpGetInfoTestCase
from .test_get_info_list import GmpGetInfoListTestCase
from .test_modify_filter import GmpModifyFilterTestCase
from .test_modify_permission import GmpModifyPermissionTestCase
from .test_modify_report_format import GmpModifyReportFormatTestCase
from .test_modify_tag import GmpModifyTagTestCase
from .test_get_feed import GmpGetFeedTestCase
from .test_clone_audit import GmpCloneAuditTestCase
from .test_clone_config import GmpCloneConfigTestCase
from .test_clone_policy import GmpClonePolicyTestCase
from .test_clone_task import GmpCloneTaskTestCase
from .test_clone_tls_certificate import GmpCloneTLSCertificateTestCase
from .test_create_audit import GmpCreateAuditCommandTestCase
from .test_create_alert import GmpCreateAlertTestCase
from .test_create_config import GmpCreateConfigTestCase
from .test_create_config_from_osp_scanner import (
    GmpCreateConfigFromOSPScannerTestCase,
)
from .test_create_credential import GmpCreateCredentialTestCase
from .test_create_policy import GmpCreatePolicyTestCase
from .test_create_scanner import GmpCreateScannerTestCase
from .test_create_task import GmpCreateTaskCommandTestCase
from .test_create_tls_certificate import GmpCreateTLSCertificateTestCase
from .test_delete_audit import GmpDeleteAuditTestCase
from .test_delete_config import GmpDeleteConfigTestCase
from .test_delete_policy import GmpDeletePolicyTestCase
from .test_delete_task import GmpDeleteTaskTestCase
from .test_delete_tls_certificate import GmpDeleteTLSCertificateTestCase
from .test_get_audit import GmpGetAuditTestCase
from .test_get_audits import GmpGetAuditsTestCase
from .test_get_config import GmpGetConfigTestCase
from .test_get_configs import GmpGetConfigsTestCase
from .test_get_policies import GmpGetPoliciesTestCase
from .test_get_policy import GmpGetPolicyTestCase
from .test_get_task import GmpGetTaskTestCase
from .test_get_tasks import GmpGetTasksTestCase
from .test_get_tls_certificate import GmpGetTlsCertificateTestCase
from .test_get_tls_certificates import GmpGetTLSCertificatesTestCase
from .test_modify_credential import GmpModifyCredentialTestCase
from .test_modify_alert import GmpModifyAlertTestCase
from .test_modify_audit import GmpModifyAuditCommandTestCase
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
from .test_modify_tls_certificate import GmpModifyTLSCertificateTestCase
from .test_resume_audit import GmpResumeAuditTestCase
from .test_start_audit import GmpStartAuditTestCase
from .test_stop_audit import GmpStopAuditTestCase
from .test_import_report import GmpImportReportTestCase
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
