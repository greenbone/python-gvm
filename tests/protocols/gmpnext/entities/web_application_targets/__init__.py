#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_web_application_target import (
    GmpCloneWebApplicationTargetTestMixin,
)
from .test_create_web_application_target import (
    GmpCreateWebApplicationTargetTestMixin,
)
from .test_delete_web_application_target import (
    GmpDeleteWebApplicationTargetTestMixin,
)
from .test_get_web_application_target import (
    GmpGetWebApplicationTargetTestMixin,
)
from .test_get_web_application_targets import (
    GmpGetWebApplicationTargetsTestMixin,
)
from .test_modify_web_application_target import (
    GmpModifyWebApplicationTargetTestMixin,
)

__all__ = (
    "GmpCloneWebApplicationTargetTestMixin",
    "GmpCreateWebApplicationTargetTestMixin",
    "GmpDeleteWebApplicationTargetTestMixin",
    "GmpGetWebApplicationTargetTestMixin",
    "GmpGetWebApplicationTargetsTestMixin",
    "GmpModifyWebApplicationTargetTestMixin",
)
