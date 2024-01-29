# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_role import GmpCloneRoleTestMixin
from .test_create_role import GmpCreateRoleTestMixin
from .test_delete_role import GmpDeleteRoleTestMixin
from .test_get_role import GmpGetRoleTestMixin
from .test_get_roles import GmpGetRolesTestMixin
from .test_modify_role import GmpModifyRoleTestMixin

__all__ = (
    "GmpCloneRoleTestMixin",
    "GmpCreateRoleTestMixin",
    "GmpDeleteRoleTestMixin",
    "GmpGetRoleTestMixin",
    "GmpGetRolesTestMixin",
    "GmpModifyRoleTestMixin",
)
