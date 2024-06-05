# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .permissions import (
    GmpClonePermissionTestMixin,
    GmpCreatePermissionTestMixin,
    GmpDeletePermissionTestMixin,
    GmpGetPermissionsTestMixin,
    GmpGetPermissionTestMixin,
    GmpModifyPermissionTestMixin,
)


class Gmpv224DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetPermissionTestCase(GmpGetPermissionTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetPermissionsTestCase(
    GmpGetPermissionsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ClonePermissionTestCase(
    GmpClonePermissionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, Gmpv224TestCase
):
    pass
