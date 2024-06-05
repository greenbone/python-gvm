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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetPermissionTestCase(GmpGetPermissionTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetPermissionsTestCase(
    GmpGetPermissionsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ClonePermissionTestCase(
    GmpClonePermissionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, Gmpv225TestCase
):
    pass
