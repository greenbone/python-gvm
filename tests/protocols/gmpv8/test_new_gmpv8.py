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
from .testcmds import *  # pylint: disable=wildcard-import


class Gmpv8CloneTicketTestCase(GmpCloneTicketTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateCredentialTestCase(GmpCreateCredentialTestCase, Gmpv8TestCase):

    pass


class Gmpv8CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreatePermissionTestCase(GmpCreatePermissionTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateTagTestCase(GmpCreateTagTestCase, Gmpv8TestCase):
    pass


class Gmpv8CreateTargetCommandTestCase(
    GmpCreateTargetCommandTestCase, Gmpv8TestCase
):
    pass


class Gmpv8CreateTicketTestCase(GmpCreateTicketTestCase, Gmpv8TestCase):
    pass


class Gmpv8DeleteTicketTestCase(GmpDeleteTicketTestCase, Gmpv8TestCase):

    pass


class Gmpv8GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTicketTestCase(GmpGetTicketTestCase, Gmpv8TestCase):
    pass


class Gmpv8GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv8TestCase):

    pass


class Gmpv8GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestCase, Gmpv8TestCase
):

    pass


class Gmpv8GetVulnerabilityTestCase(GmpGetVulnerabilityTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv8TestCase
):
    pass


class Gmpv8ModifyTestCase(GmpModifyTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv8TestCase):

    pass


class Gmpv8ModifyPermissionTestCase(GmpModifyPermissionTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyTagTestCase(GmpModifyTagTestCase, Gmpv8TestCase):
    pass


class Gmpv8ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv8TestCase):
    pass


class Gmpv8ProtocolVersionTestCase(GmpProtocolVersionTestCase, Gmpv8TestCase):
    pass
