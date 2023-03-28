# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
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

from gvm.protocols.gmpv208.entities.hosts import HostsOrdering

from . import Gmpv208TestCase


class GmpWithStatementTestMixin:
    def test_types(self):
        with self.gmp:
            # Test that the values are equal
            self.assertEqual(
                self.gmp.types.AlertEvent.TASK_RUN_STATUS_CHANGED.value,
                "Task run status changed",
            )
            self.assertEqual(
                self.gmp.types.PermissionSubjectType.USER.value, "user"
            )
            self.assertEqual(
                self.gmp.types.HostsOrdering.RANDOM.value, "random"
            )

            # Test usability of from_string
            self.assertEqual(
                self.gmp.types.HostsOrdering.from_string("reverse"),
                self.gmp.types.HostsOrdering.REVERSE,
            )

            # Test, that the Enum class types are equal
            self.assertEqual(self.gmp.types.HostsOrdering, HostsOrdering)


class Gmpv208WithStatementTestCase(GmpWithStatementTestMixin, Gmpv208TestCase):
    pass
