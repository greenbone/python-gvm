# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.protocols.gmpv208.entities.hosts import HostsOrdering

from . import Gmpv214TestCase


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


class Gmpv214WithStatementTestCase(GmpWithStatementTestMixin, Gmpv214TestCase):
    pass
