# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_group import GmpCloneGroupTestMixin
from .test_create_group import GmpCreateGroupTestMixin
from .test_delete_group import GmpDeleteGroupTestMixin
from .test_get_group import GmpGetGroupTestMixin
from .test_get_groups import GmpGetGroupsTestMixin
from .test_modify_group import GmpModifyGroupTestMixin

__all__ = (
    "GmpCloneGroupTestMixin",
    "GmpCreateGroupTestMixin",
    "GmpDeleteGroupTestMixin",
    "GmpGetGroupTestMixin",
    "GmpGetGroupsTestMixin",
    "GmpModifyGroupTestMixin",
)
