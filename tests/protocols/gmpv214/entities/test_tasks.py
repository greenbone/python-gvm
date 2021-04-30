# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ...gmpv214 import Gmpv214TestCase
from ...gmpv208.entities.tasks import (
    GmpCloneTaskTestCase,
    GmpCreateContainerTaskTestCase,
    GmpCreateTaskTestCase,
    GmpDeleteTaskTestCase,
    GmpGetTasksTestCase,
    GmpGetTaskTestCase,
    GmpModifyTaskTestCase,
    GmpMoveTaskTestCase,
    GmpResumeTaskTestCase,
    GmpStartTaskTestCase,
    GmpStopTaskTestCase,
)


class Gmpv214CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateTaskTestCase(GmpCreateTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTaskTestCase(GmpGetTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetTasksTestCase(GmpGetTasksTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyTaskTestCase(GmpModifyTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214ResumeTaskTestCase(GmpResumeTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214StartTaskTestCase(GmpStartTaskTestCase, Gmpv214TestCase):
    pass


class Gmpv214StopTaskTestCase(GmpStopTaskTestCase, Gmpv214TestCase):
    pass
