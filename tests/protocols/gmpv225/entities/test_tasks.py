# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.tasks import (
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
from ...gmpv225 import GMPTestCase


class Gmpv225CloneTaskTestCase(GmpCloneTaskTestMixin, GMPTestCase):
    pass


class Gmpv225CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, GMPTestCase
):
    pass


class Gmpv225CreateTaskTestCase(GmpCreateTaskTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteTaskTestCase(GmpDeleteTaskTestMixin, GMPTestCase):
    pass


class Gmpv225GetTaskTestCase(GmpGetTaskTestMixin, GMPTestCase):
    pass


class Gmpv225GetTasksTestCase(GmpGetTasksTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyTaskTestCase(GmpModifyTaskTestMixin, GMPTestCase):
    pass


class Gmpv225MoveTaskTestCase(GmpMoveTaskTestMixin, GMPTestCase):
    pass


class Gmpv225ResumeTaskTestCase(GmpResumeTaskTestMixin, GMPTestCase):
    pass


class Gmpv225StartTaskTestCase(GmpStartTaskTestMixin, GMPTestCase):
    pass


class Gmpv225StopTaskTestCase(GmpStopTaskTestMixin, GMPTestCase):
    pass
