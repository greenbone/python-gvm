# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.permissions import (
    GmpClonePermissionTestMixin,
    GmpCreatePermissionTestMixin,
    GmpDeletePermissionTestMixin,
    GmpGetPermissionsTestMixin,
    GmpGetPermissionTestMixin,
    GmpModifyPermissionTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetPermissionTestCase(GmpGetPermissionTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPermissionsTestCase(
    GmpGetPermissionsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ClonePermissionTestCase(
    GmpClonePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, Gmpv214TestCase
):
    pass
