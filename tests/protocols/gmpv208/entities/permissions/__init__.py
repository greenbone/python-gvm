# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_permission import GmpClonePermissionTestMixin
from .test_create_permission import GmpCreatePermissionTestMixin
from .test_delete_permission import GmpDeletePermissionTestMixin
from .test_get_permission import GmpGetPermissionTestMixin
from .test_get_permissions import GmpGetPermissionsTestMixin
from .test_modify_permission import GmpModifyPermissionTestMixin

__all__ = (
    "GmpClonePermissionTestMixin",
    "GmpCreatePermissionTestMixin",
    "GmpDeletePermissionTestMixin",
    "GmpGetPermissionTestMixin",
    "GmpGetPermissionsTestMixin",
    "GmpModifyPermissionTestMixin",
)
