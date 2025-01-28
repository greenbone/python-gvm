# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.permissions import (
    GmpClonePermissionTestMixin,
    GmpCreatePermissionTestMixin,
    GmpDeletePermissionTestMixin,
    GmpGetPermissionsTestMixin,
    GmpGetPermissionTestMixin,
    GmpModifyPermissionTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, GMPTestCase
):
    pass


class Gmpv225GetPermissionTestCase(GmpGetPermissionTestMixin, GMPTestCase):
    pass


class Gmpv225GetPermissionsTestCase(GmpGetPermissionsTestMixin, GMPTestCase):
    pass


class Gmpv225ClonePermissionTestCase(GmpClonePermissionTestMixin, GMPTestCase):
    pass


class Gmpv225CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, GMPTestCase
):
    pass
