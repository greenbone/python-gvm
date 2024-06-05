# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.roles import (
    GmpCloneRoleTestMixin,
    GmpCreateRoleTestMixin,
    GmpDeleteRoleTestMixin,
    GmpGetRolesTestMixin,
    GmpGetRoleTestMixin,
    GmpModifyRoleTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetRoleTestCase(GmpGetRoleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetRolesTestCase(GmpGetRolesTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv225TestCase):
    pass
