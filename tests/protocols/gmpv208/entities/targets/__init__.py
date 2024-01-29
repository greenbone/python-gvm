# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_target import GmpCloneTargetTestMixin
from .test_create_target import GmpCreateTargetTestMixin
from .test_delete_target import GmpDeleteTargetTestMixin
from .test_get_target import GmpGetTargetTestMixin
from .test_get_targets import GmpGetTargetsTestMixin
from .test_modify_target import GmpModifyTargetTestMixin

__all__ = (
    "GmpCloneTargetTestMixin",
    "GmpCreateTargetTestMixin",
    "GmpDeleteTargetTestMixin",
    "GmpGetTargetTestMixin",
    "GmpGetTargetsTestMixin",
    "GmpModifyTargetTestMixin",
)
