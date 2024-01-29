# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .permissions import (
    GmpClonePermissionTestMixin,
    GmpCreatePermissionTestMixin,
    GmpDeletePermissionTestMixin,
    GmpGetPermissionsTestMixin,
    GmpGetPermissionTestMixin,
    GmpModifyPermissionTestMixin,
)


class Gmpv208DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetPermissionTestCase(GmpGetPermissionTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetPermissionsTestCase(
    GmpGetPermissionsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ClonePermissionTestCase(
    GmpClonePermissionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, Gmpv208TestCase
):
    pass
