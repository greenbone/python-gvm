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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetRoleTestCase(GmpGetRoleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetRolesTestCase(GmpGetRolesTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv224TestCase):
    pass
