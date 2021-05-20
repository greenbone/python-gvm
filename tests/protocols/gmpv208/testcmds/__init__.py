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

from .test_protocol_version import GmpProtocolVersionTestCase

from .test_empty_trashcan import GmpEmptyTrashcanCommandTestCase
from .test_get_system_reports import GmpGetSystemReportsTestCase
from .test_get_version import GmpGetVersionCommandTestCase
from .test_help import GmpHelpTestCase
from .test_restore_from_trashcan import GmpRestoreTestCase
from .test_with_statement import GmpWithStatementTestCase
