# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_task import GmpCloneTaskTestMixin
from .test_create_container_task import GmpCreateContainerTaskTestMixin
from .test_create_task import GmpCreateTaskTestMixin
from .test_delete_task import GmpDeleteTaskTestMixin
from .test_get_task import GmpGetTaskTestMixin
from .test_get_tasks import GmpGetTasksTestMixin
from .test_modify_task import GmpModifyTaskTestMixin
from .test_move_task import GmpMoveTaskTestMixin
from .test_resume_task import GmpResumeTaskTestMixin
from .test_start_task import GmpStartTaskTestMixin
from .test_stop_task import GmpStopTaskTestMixin

__all__ = (
    "GmpCloneTaskTestMixin",
    "GmpCreateContainerTaskTestMixin",
    "GmpCreateTaskTestMixin",
    "GmpDeleteTaskTestMixin",
    "GmpGetTaskTestMixin",
    "GmpGetTasksTestMixin",
    "GmpModifyTaskTestMixin",
    "GmpMoveTaskTestMixin",
    "GmpResumeTaskTestMixin",
    "GmpStartTaskTestMixin",
    "GmpStopTaskTestMixin",
)
