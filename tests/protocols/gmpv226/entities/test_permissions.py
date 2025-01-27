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
from ...gmpv226 import GMPTestCase


class GMPDeletePermissionTestCase(GmpDeletePermissionTestMixin, GMPTestCase):
    pass


class GMPGetPermissionTestCase(GmpGetPermissionTestMixin, GMPTestCase):
    pass


class GMPGetPermissionsTestCase(GmpGetPermissionsTestMixin, GMPTestCase):
    pass


class GMPClonePermissionTestCase(GmpClonePermissionTestMixin, GMPTestCase):
    pass


class GMPCreatePermissionTestCase(GmpCreatePermissionTestMixin, GMPTestCase):
    pass


class GMPModifyPermissionTestCase(GmpModifyPermissionTestMixin, GMPTestCase):
    pass
