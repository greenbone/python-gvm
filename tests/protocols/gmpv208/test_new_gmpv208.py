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


class Gmpv208ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv208TestCase):
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


class Gmpv208CloneReportFormatTestCase(
    GmpCloneReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208HelpTestCase(GmpHelpTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneGroupTestCase(GmpCloneGroupTestCase, Gmpv208TestCase):

    pass


class Gmpv208CloneRoleTestCase(GmpCloneRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208CloneScheduleTestCase(GmpCloneScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateGroupTestCase(GmpCreateGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateRoleTestCase(GmpCreateRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteGroupTestCase(GmpDeleteGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208DeleteRoleTestCase(GmpDeleteRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteScheduleTestCase(GmpDeleteScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetGroupTestCase(GmpGetGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetGroupsTestCase(GmpGetGroupsTestCase, Gmpv208TestCase):
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


class Gmpv208GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ImportReportFormatTestCase(
    GmpImportReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyGroupTestCase(GmpModifyGroupTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyRoleTestCase(GmpModifyRoleTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifySettingTestCase(GmpModifySettingTestCase, Gmpv208TestCase):
    pass


class Gmpv208RestoreTestCase(GmpRestoreTestCase, Gmpv208TestCase):
    pass


class Gmpv208SyncCertCommandTestCase(
    GmpSyncCertCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208SyncScapCommandTestCase(
    GmpSyncScapCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestCase, Gmpv208TestCase
):
    pass


class Gmpv208v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv208TestCase):
    pass
