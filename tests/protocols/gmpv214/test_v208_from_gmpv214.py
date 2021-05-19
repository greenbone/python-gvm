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


class Gmpv214GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv214TestCase):
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


class Gmpv214CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CloneFilterTestCase(GmpCloneFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214HelpTestCase(GmpHelpTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv214TestCase):

    pass


class Gmpv214CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteFilterTestCase(GmpDeleteFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv214TestCase):
    pass


class Gmpv214DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetFilterTestCase(GmpGetFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetFiltersTestCase(GmpGetFiltersTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetGroupTestCase(GmpGetGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv214TestCase):
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


class Gmpv214GetRoleTestCase(GmpGetRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetRolesTestCase(GmpGetRolesTestCase, Gmpv214TestCase):
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


class Gmpv214GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifySettingTestCase(GmpModifySettingTestCase, Gmpv214TestCase):
    pass


class Gmpv214RestoreTestCase(GmpRestoreTestCase, Gmpv214TestCase):
    pass


class Gmpv214SyncCertCommandTestCase(
    GmpSyncCertCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214SyncScapCommandTestCase(
    GmpSyncScapCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv214TestCase):
    pass
