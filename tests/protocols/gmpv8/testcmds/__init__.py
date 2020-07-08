# -*- coding utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from .test_clone_ticket import GmpCloneTicketTestCase
from .test_create_credential import GmpCreateCredentialTestCase
from .test_create_filter import GmpCreateFilterTestCase
from .test_create_permission import GmpCreatePermissionTestCase
from .test_create_schedule import GmpCreateScheduleTestCase
from .test_create_tag import GmpCreateTagTestCase
from .test_create_target import GmpCreateTargetCommandTestCase
from .test_create_ticket import GmpCreateTicketTestCase
from .test_delete_ticket import GmpDeleteTicketTestCase
from .test_get_aggregates import GmpGetAggregatesTestCase
from .test_get_ticket import GmpGetTicketTestCase
from .test_get_tickets import GmpGetTargetsTestCase
from .test_get_vulnerabilities import GmpGetVulnerabilitiesTestCase
from .test_get_vulnerability import GmpGetVulnerabilityTestCase
from .test_modify_credential import GmpModifyTestCase
from .test_modify_filter import GmpModifyFilterTestCase
from .test_modify_permission import GmpModifyPermissionTestCase
from .test_modify_schedule import GmpModifyScheduleTestCase
from .test_modify_tag import GmpModifyTagTestCase
from .test_modify_ticket import GmpModifyTicketTestCase
from .test_protocol_version import GmpProtocolVersionTestCase
