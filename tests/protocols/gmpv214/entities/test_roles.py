# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.roles import (
    GmpCloneRoleTestMixin,
    GmpCreateRoleTestMixin,
    GmpDeleteRoleTestMixin,
    GmpGetRolesTestMixin,
    GmpGetRoleTestMixin,
    GmpModifyRoleTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetRoleTestCase(GmpGetRoleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetRolesTestCase(GmpGetRolesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv214TestCase):
    pass
