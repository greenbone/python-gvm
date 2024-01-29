# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_tag import GmpCloneTagTestMixin
from .test_create_tag import GmpCreateTagTestMixin
from .test_delete_tag import GmpDeleteTagTestMixin
from .test_get_tag import GmpGetTagTestMixin
from .test_get_tags import GmpGetTagsTestMixin
from .test_modify_tag import GmpModifyTagTestMixin

__all__ = (
    "GmpCloneTagTestMixin",
    "GmpCreateTagTestMixin",
    "GmpDeleteTagTestMixin",
    "GmpGetTagTestMixin",
    "GmpGetTagsTestMixin",
    "GmpModifyTagTestMixin",
)
