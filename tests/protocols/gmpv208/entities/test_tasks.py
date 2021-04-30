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

from ...gmpv208 import Gmpv208TestCase
from .tasks import (
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


class Gmpv208CloneTaskTestCase(GmpCloneTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateTaskTestCase(GmpCreateTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteTaskTestCase(GmpDeleteTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTaskTestCase(GmpGetTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTasksTestCase(GmpGetTasksTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyTaskTestCase(GmpModifyTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208MoveTaskTestCase(GmpMoveTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208ResumeTaskTestCase(GmpResumeTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208StartTaskTestCase(GmpStartTaskTestCase, Gmpv208TestCase):
    pass


class Gmpv208StopTaskTestCase(GmpStopTaskTestCase, Gmpv208TestCase):
    pass
