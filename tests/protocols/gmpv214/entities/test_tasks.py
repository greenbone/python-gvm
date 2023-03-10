# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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
