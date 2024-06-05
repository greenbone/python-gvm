# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .tasks import (
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


class Gmpv224CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTaskTestCase(GmpGetTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTasksTestCase(GmpGetTasksTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StartTaskTestCase(GmpStartTaskTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StopTaskTestCase(GmpStopTaskTestMixin, Gmpv224TestCase):
    pass
