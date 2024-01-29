# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_delete_operating_system import GmpDeleteOperatingSystemTestMixin
from .test_get_operating_system import GmpGetOperatingSystemTestMixin
from .test_get_operating_systems import GmpGetOperatingSystemsTestMixin
from .test_modify_operating_system import GmpModifyOperatingSystemTestMixin

__all__ = (
    "GmpDeleteOperatingSystemTestMixin",
    "GmpGetOperatingSystemTestMixin",
    "GmpGetOperatingSystemsTestMixin",
    "GmpModifyOperatingSystemTestMixin",
)
