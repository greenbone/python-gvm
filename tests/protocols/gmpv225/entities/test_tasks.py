# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.tasks import (
    GmpCloneTaskTestMixin,
    GmpCreateContainerTaskTestMixin,
    GmpCreateTaskTestMixin,
    GmpDeleteTaskTestMixin,
    GmpGetTasksTestMixin,
    GmpGetTaskTestMixin,
    GmpModifyTaskTestMixin,
    GmpMoveTaskTestMixin,
    GmpResumeTaskTestMixin,
    GmpStartTaskTestMixin,
    GmpStopTaskTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTaskTestCase(GmpGetTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTasksTestCase(GmpGetTasksTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StartTaskTestCase(GmpStartTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StopTaskTestCase(GmpStopTaskTestMixin, Gmpv225TestCase):
    pass
