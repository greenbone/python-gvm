# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_schedule import GmpCloneScheduleTestMixin
from .test_create_schedule import GmpCreateScheduleTestMixin
from .test_delete_schedule import GmpDeleteScheduleTestMixin
from .test_get_schedule import GmpGetScheduleTestMixin
from .test_get_schedules import GmpGetSchedulesTestMixin
from .test_modify_schedule import GmpModifyScheduleTestMixin

__all__ = (
    "GmpCloneScheduleTestMixin",
    "GmpCreateScheduleTestMixin",
    "GmpDeleteScheduleTestMixin",
    "GmpGetScheduleTestMixin",
    "GmpGetSchedulesTestMixin",
    "GmpModifyScheduleTestMixin",
)
