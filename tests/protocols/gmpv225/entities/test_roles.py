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
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteRoleTestCase(GmpDeleteRoleTestMixin, GMPTestCase):
    pass


class Gmpv225GetRoleTestCase(GmpGetRoleTestMixin, GMPTestCase):
    pass


class Gmpv225GetRolesTestCase(GmpGetRolesTestMixin, GMPTestCase):
    pass


class Gmpv225CloneRoleTestCase(GmpCloneRoleTestMixin, GMPTestCase):
    pass


class Gmpv225CreateRoleTestCase(GmpCreateRoleTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyRoleTestCase(GmpModifyRoleTestMixin, GMPTestCase):
    pass
