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
from ...gmpv226 import GMPTestCase


class GMPDeleteRoleTestCase(GmpDeleteRoleTestMixin, GMPTestCase):
    pass


class GMPGetRoleTestCase(GmpGetRoleTestMixin, GMPTestCase):
    pass


class GMPGetRolesTestCase(GmpGetRolesTestMixin, GMPTestCase):
    pass


class GMPCloneRoleTestCase(GmpCloneRoleTestMixin, GMPTestCase):
    pass


class GMPCreateRoleTestCase(GmpCreateRoleTestMixin, GMPTestCase):
    pass


class GMPModifyRoleTestCase(GmpModifyRoleTestMixin, GMPTestCase):
    pass
