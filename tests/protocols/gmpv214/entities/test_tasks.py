# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTaskTestCase(GmpGetTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTasksTestCase(GmpGetTasksTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StartTaskTestCase(GmpStartTaskTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StopTaskTestCase(GmpStopTaskTestMixin, Gmpv214TestCase):
    pass
