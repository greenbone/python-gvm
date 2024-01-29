# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .roles import (
    GmpCloneRoleTestMixin,
    GmpCreateRoleTestMixin,
    GmpDeleteRoleTestMixin,
    GmpGetRolesTestMixin,
    GmpGetRoleTestMixin,
    GmpModifyRoleTestMixin,
)


class Gmpv208DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetRoleTestCase(GmpGetRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetRolesTestCase(GmpGetRolesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv208TestCase):
    pass
