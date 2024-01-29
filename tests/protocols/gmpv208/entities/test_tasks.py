# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
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


class Gmpv208CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTaskTestCase(GmpGetTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTasksTestCase(GmpGetTasksTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208StartTaskTestCase(GmpStartTaskTestMixin, Gmpv208TestCase):
    pass


class Gmpv208StopTaskTestCase(GmpStopTaskTestMixin, Gmpv208TestCase):
    pass
